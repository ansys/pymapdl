/**
 * @file search-main.js
 * @description Main search logic for the documentation site. Handles search index
 * loading, filtering, and UI updates. Uses Fuse.js for fuzzy searching and
 * IndexedDB for caching search data.
 */

const SEARCH_BAR = document.getElementById("search-bar");

require.config({
  paths: {
    fuse: "https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.min",
  },
});

/**
 * Open or create an IndexedDB database for caching search indexes.
 * @param {string} name - Database name.
 * @param {number} version - Database version.
 * @returns {Promise<IDBDatabase>}
 */
function openDB(name = "search-cache", version = 1) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(name, version);
    request.onerror = () => {
      console.error("IndexedDB open error:", request.error);
      reject(request.error);
    };
    request.onsuccess = () => {
      resolve(request.result);
    };
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("indexes")) {
        db.createObjectStore("indexes");
      }
    };
  });
}

/**
 * Retrieve a cached value from IndexedDB by key.
 * @param {string} key
 * @returns {Promise<any>}
 */
async function getFromIDB(key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("indexes", "readonly");
    const store = transaction.objectStore("indexes");
    const request = store.get(key);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/**
 * Save a key-value pair to IndexedDB.
 * @param {string} key
 * @param {any} value
 * @returns {Promise<boolean>}
 */
async function saveToIDB(key, value) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction("indexes", "readwrite");
    const store = transaction.objectStore("indexes");
    const request = store.put(value, key);
    request.onsuccess = () => resolve(true);
    request.onerror = () => {
      console.error("Failed to save to IndexedDB:", request.error);
      reject(request.error);
    };
  });
}

require(["fuse"], function (Fuse) {
  let fuse;
  let searchData = [];
  let selectedObjectIDs = [];
  let selectedLibraries = [];
  const libSearchData = {};
  let selectedFilter = new Set();
  const searchPageContainer = document.querySelector(".bd-search-container");

  /**
   * @param {Function} func
   * @param {number} delay
   * @returns {Function}
   */
  const debounce = (func, delay) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), delay);
    };
  };

  /**
   * Load the main search index and all library indexes, then set up the filter UI.
   */
  async function initializeSearch() {
    // Build sidebar scaffolding early so filter UI is visible even if
    // search index/network loading fails.
    setupFilterDropdown();
    if (Object.keys(EXTRA_SOURCES).length > 0) {
      showLibraryDropdown();
    }

    try {
      const cacheKey = "main-search-index";
      let data = await getFromIDB(cacheKey);
      if (!data) {
        const response = await fetch(SEARCH_FILE);
        data = await response.json();
        await saveToIDB(cacheKey, data);
      }
      searchData = data;
      fuse = new Fuse(searchData, SEARCH_OPTIONS);

      // Render filter UI immediately after the main index is ready.
      // External library fetch failures should not block sidebar rendering.
      showObjectIdDropdown();

      // Load library search data
      const allLibs = Object.keys(EXTRA_SOURCES);
      for (const lib of allLibs) {
        try {
          const cacheKey = `lib-search-${lib}`;
          let libData = await getFromIDB(cacheKey);
          if (!libData) {
            const libPath = EXTRA_SOURCES[lib];
            const url = `${libPath}/_static/search.json`;
            const res = await fetch(url);
            libData = await res.json();
            await saveToIDB(cacheKey, libData);
          }
          libSearchData[lib] = libData;
        } catch (libErr) {
          console.warn(`Failed to preload library index for ${lib}:`, libErr);
        }
      }
    } catch (err) {
      console.error("Search init failed", err);
    }
  }

  /**
   * Build the filter sidebar: toggle sections for Documents and Library filters.
   */
  function setupFilterDropdown() {
    const dropdownContainer =
      searchPageContainer?.querySelector("#search-sidebar") ||
      document.getElementById("search-sidebar");
    if (!dropdownContainer) {
      console.warn("Search sidebar container not found; filters are disabled.");
      return;
    }
    dropdownContainer.innerHTML = "";
    const filters = [
      {
        name: "Documents",
        dropdownId: "objectid-dropdown",
        callback: showObjectIdDropdown,
      },
      {
        name: "Library",
        dropdownId: "library-dropdown",
        callback: showLibraryDropdown,
      },
    ];
    // Remove the library filter if no libraries
    if (Object.keys(EXTRA_SOURCES).length === 0) {
      filters.splice(1, 1);
    }
    filters.forEach(({ name, dropdownId, callback }) => {
      const toggleDiv = document.createElement("div");
      toggleDiv.className = "search-page-sidebar toggle-section";
      toggleDiv.dataset.target = dropdownId;
      const icon = document.createElement("span");
      icon.className = "toggle-icon";
      icon.textContent = "▼";
      icon.style.fontSize = "12px";
      const label = document.createElement("span");
      label.className = "toggle-label";
      label.textContent = name;
      toggleDiv.append(icon, label);
      const dropdown = document.createElement("div");
      dropdown.id = dropdownId;
      dropdown.className = "dropdown-menu show";
      dropdown.style.display = "block";
      dropdown.style.marginTop = "10px";
      // Add event listener to toggle the dropdown
      toggleDiv.addEventListener("click", () => {
        const isVisible = dropdown.style.display === "block";
        dropdown.style.display = isVisible ? "none" : "block";
        icon.textContent = isVisible ? "▶" : "▼";
        if (isVisible) {
          selectedFilter.delete(name);
          toggleDiv.classList.remove("active");
        } else {
          selectedFilter.add(name);
          toggleDiv.classList.add("active");
          callback?.();
        }
        performSearch();
      });
      dropdownContainer.append(toggleDiv, dropdown);
    });
  }

  /**
   * Populate the Documents filter dropdown with objectID checkboxes.
   */
  function showObjectIdDropdown() {
    const dropdown = document.getElementById("objectid-dropdown");
    if (!dropdown) return;
    dropdown.innerHTML = "";
    const objectIDs = [
      ...new Set(searchData.map((item) => item.objectID)),
    ].filter(Boolean);
    objectIDs.forEach((id) => {
      const checkbox = createCheckboxItem(id, selectedObjectIDs, () => {
        renderSelectedChips();
        performSearch();
      });
      dropdown.appendChild(checkbox);
    });
    dropdown.style.display = "block";
    renderSelectedChips();
  }

  /**
   * Populate the Library filter dropdown with one checkbox per extra source.
   */
  function showLibraryDropdown() {
    const dropdown = document.getElementById("library-dropdown");
    if (!dropdown) return;
    dropdown.innerHTML = "";
    for (const lib in EXTRA_SOURCES) {
      const checkbox = createCheckboxItem(lib, selectedLibraries, () => {
        renderSelectedChips();
        performSearch();
      });
      dropdown.appendChild(checkbox);
    }
    dropdown.style.display = "block";
    renderSelectedChips();
  }

  /**
   * Create a labelled checkbox element for a filter dropdown.
   * @param {string} value
   * @param {Array} selectedArray - Mutated in-place on toggle.
   * @param {Function} onChange
   * @returns {HTMLDivElement}
   */
  function createCheckboxItem(value, selectedArray, onChange) {
    const div = document.createElement("div");
    div.className = "checkbox-item";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = value;
    checkbox.style.margin = "8px";
    checkbox.checked = selectedArray.includes(value);
    checkbox.onchange = (e) => {
      if (e.target.checked) {
        selectedArray.push(value);
      } else {
        const index = selectedArray.indexOf(value);
        if (index > -1) selectedArray.splice(index, 1);
      }
      onChange();
    };
    const label = document.createElement("label");
    label.textContent = value;
    div.appendChild(checkbox);
    div.appendChild(label);
    return div;
  }

  /**
   * Re-render the row of chips that represent active filter selections.
   */
  function renderSelectedChips() {
    const container = document.getElementById("selected-chips");
    container.innerHTML = "";
    const renderChip = (value, type, selectedArray) => {
      const chip = document.createElement("div");
      chip.className = "chip";
      chip.textContent = `${value} (${type})`;
      const removeBtn = document.createElement("button");
      removeBtn.className = "remove-btn";
      removeBtn.innerHTML = "&times;";
      removeBtn.onclick = () => {
        const index = selectedArray.indexOf(value);
        if (index !== -1) selectedArray.splice(index, 1);
        renderSelectedChips();
        if (type === "Documents") showObjectIdDropdown();
        if (type === "Library") showLibraryDropdown();
        performSearch();
      };
      chip.appendChild(removeBtn);
      container.appendChild(chip);
    };
    selectedObjectIDs.forEach((id) =>
      renderChip(id, "Documents", selectedObjectIDs),
    );
    selectedLibraries.forEach((lib) =>
      renderChip(lib, "Library", selectedLibraries),
    );
  }

  /**
   * Compute a relevance score for a Fuse.js result.
   * Fuse score: 0 = perfect match, 1 = complete mismatch; boosted by matched field weight.
   * @param {Object} result - Fuse.js result with .score and .matches.
   * @returns {number}
   */
  function computeRelevance(result) {
    // Build weight map from SEARCH_OPTIONS.keys
    const configKeys = Array.isArray(SEARCH_OPTIONS.keys)
      ? SEARCH_OPTIONS.keys
      : [];
    const fieldWeights = configKeys.length
      ? Object.fromEntries(configKeys.map((k) => [k.name, k.weight ?? 1]))
      : { section: 3, title: 3, text: 1, objectID: 0.5 };
    const matches = result.matches || [];
    const fieldWeight = matches.length
      ? Math.max(...matches.map((m) => fieldWeights[m.key] || 1))
      : 1;
    return (1 - (result.score || 0)) * fieldWeight;
  }

  /**
   * Run the current query against all indexes and update the results UI.
   */
  async function performSearch() {
    const query = document.getElementById("search-input").value.trim();
    if (!fuse) return;
    const url = new URL(window.location);
    url.searchParams.set("q", query);
    history.replaceState({}, "", url);
    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = "Searching...";
    let docResults = [];
    let libResults = [];
    const resultLimit = getSelectedResultLimit();
    if (selectedFilter.size === 0 || selectedFilter.has("Documents")) {
      // Filter first, then apply the result limit so selected document filters
      // are not accidentally dropped by early truncation.
      docResults = fuse
        .search(query)
        .sort((a, b) => computeRelevance(b) - computeRelevance(a))
        .map((r) => r.item);
      if (selectedObjectIDs.length > 0) {
        docResults = docResults.filter((item) =>
          selectedObjectIDs.includes(item.objectID),
        );
      }
      docResults = docResults.slice(0, resultLimit);
    }
    // Search in selected libraries — apply the same re-ranking as doc results.
    // Reference: https://www.fusejs.io/api/options.html#keys
    for (const lib of selectedLibraries) {
      const libBaseUrl = EXTRA_SOURCES[lib];
      const cacheKey = `lib-search-${lib}`;
      try {
        let data = await getFromIDB(cacheKey);
        if (!data) {
          const url = `${libBaseUrl}/_static/search.json`;
          const res = await fetch(url);
          if (res.ok) {
            data = await res.json();
            await saveToIDB(cacheKey, data);
          }
        }
        if (data) {
          const enrichedEntries = data.map((entry) => ({
            title: entry.title,
            text: entry.text,
            section: entry.section,
            link: `${libBaseUrl}${entry.href}`,
            source: lib,
          }));
          const libFuse = new Fuse(enrichedEntries, SEARCH_OPTIONS);
          const results = libFuse
            .search(query, { limit: resultLimit })
            .sort((a, b) => computeRelevance(b) - computeRelevance(a))
            .slice(0, resultLimit)
            .map((r) => r.item);
          libResults.push(...results);
        }
      } catch (err) {
        console.error(`Error accessing cache for ${lib}:`, err);
      }
    }
    // Merge and show results
    const mergedResults = [...docResults, ...libResults];
    if (mergedResults.length === 0) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }
    const highlightedResults = highlightResults(mergedResults, query);
    displayResults(highlightedResults);
  }

  /**
   * Wrap matched terms in <span class="search-highlight"> and trim body text to a context snippet.
   * @param {Array} results
   * @param {string} query
   * @returns {Array}
   */
  function highlightResults(results, query) {
    const regex = new RegExp(`(${query})`, "gi");
    return results.map((result) => {
      // Find the query in the body text first for a context snippet.
      // If the match is only in title/section, still include the result
      const text = result.text || "";
      const matchIndex = text.toLowerCase().indexOf(query.toLowerCase());
      let highlightedText = "";
      if (matchIndex !== -1) {
        const contextLength = 100;
        const start = Math.max(0, matchIndex - contextLength);
        const end = Math.min(text.length, matchIndex + contextLength);
        let snippet = text.slice(start, end);
        if (start > 0) snippet = "…" + snippet;
        if (end < text.length) snippet += "…";
        highlightedText = snippet.replace(
          regex,
          `<span class="search-highlight">$1</span>`,
        );
      }
      return {
        ...result,
        title: result.title.replace(
          regex,
          `<span class="search-highlight">$1</span>`,
        ),
        text: highlightedText,
      };
    });
  }

  /**
   * Render result cards into the results container.
   * @param {Array} results
   */
  function displayResults(results) {
    const container = document.getElementById("search-results");
    container.innerHTML = "";
    results.forEach((item) => {
      const div = document.createElement("div");
      div.className = "result-item";
      const title = document.createElement("a");
      title.href = item.href || item.link || "#";
      title.target = "_blank";
      title.innerHTML = item.title || "Untitled";
      title.className = "result-title";
      div.appendChild(title);
      if (item.text) {
        const text = document.createElement("p");
        text.innerHTML = item.text;
        text.className = "result-text";
        div.appendChild(text);
      }
      if (item.source) {
        const source = document.createElement("p");
        source.className = "checkmark";
        source.textContent = `Source: ${item.source}`;
        div.appendChild(source);
      }
      container.appendChild(div);
    });
  }

  /**
   * Read the selected page-size value from the result-limit dropdown.
   * @returns {number}
   */
  function getSelectedResultLimit() {
    const select = document.getElementById("result-limit");
    return parseInt(select.value, 10) || 10;
  }

  const handleSearchInput = debounce(
    () => {
      const query = document.getElementById("search-input").value.trim();
      if (query.length > 0) {
        performSearch();
      }
    },
    parseInt(SEARCH_OPTIONS.delay) || 300,
  );

  const $ = (id) => document.getElementById(id);

  // Elements
  const searchInput = $("search-input");
  const resultLimit = $("result-limit");

  // Initialize search input if query param is present
  const urlParams = new URLSearchParams(window.location.search);
  const initialQuery = urlParams.get("q");
  if (initialQuery && searchInput) {
    searchInput.value = initialQuery;
  }

  const triggerSearch = () => {
    if (!searchInput) return;
    const query = searchInput.value.trim();
    if (query) {
      handleSearchInput();
    } else {
      document.getElementById("search-results").innerHTML = "";
      const url = new URL(window.location);
      url.searchParams.delete("q");
      history.replaceState({}, "", url);
    }
  };

  // Set up event listeners
  searchInput?.addEventListener("input", triggerSearch);
  resultLimit?.addEventListener("change", performSearch);
  SEARCH_BAR?.addEventListener("input", (e) => {
    if (!searchInput || e.target === searchInput) {
      triggerSearch();
      return;
    }
    if (typeof e.target?.value === "string") {
      searchInput.value = e.target.value;
      triggerSearch();
    }
  });

  // Initialize search engine/data
  initializeSearch();

  // Optional: trigger on page load if query param was present
  if (initialQuery) {
    triggerSearch();
  }
});
