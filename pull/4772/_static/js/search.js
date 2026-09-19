/**
 * @file search.js
 * @description Client-side search functionality using Fuse.js for the Ansys Sphinx Theme.
 */

const MAIN_PAGE_CONTENT = document.querySelector(".bd-main");
const FUSE_VERSION = "6.4.6";
let SEARCH_BAR,
  RESULTS_CONTAINER,
  SEARCH_INPUT,
  CURRENT_INDEX = -1,
  fuseInstance;

/**
 * Load fuse.js from CDN and initialize search functionality.
 */
/**
 * Load fuse.js from CDN and initialize search functionality.
 */
require.config({
  paths: {
    fuse: `https://cdn.jsdelivr.net/npm/fuse.js@${FUSE_VERSION}/dist/fuse.min`,
  },
});

require(["fuse"], (Fuse) => {
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
   * Truncate text to a preview snippet.
   * @param {string} text
   * @param {number} maxLength
   * @returns {string}
   */
  const truncateTextPreview = (text, maxLength = 200) =>
    text.length <= maxLength ? text : `${text.slice(0, maxLength)}...`;

  /**
   * Resolve a doc-relative path using Sphinx's data-content_root attribute.
   * @param {string} targetFile
   * @returns {string}
   */
  const getDynamicPath = (targetFile) => {
    const contentRoot =
      document.documentElement.getAttribute("data-content_root");
    return `${contentRoot}${targetFile}`;
  };

  /** @param {string} href */
  const navigateToHref = (href) => {
    window.location.href = getDynamicPath(href);
  };

  /** Expand the search input and show the results overlay. */
  function expandSearchInput() {
    RESULTS_CONTAINER.style.display = "flex";
    SEARCH_INPUT.classList.add("expanded");
    MAIN_PAGE_CONTENT.classList.add("blurred");
    SEARCH_INPUT.focus();

    // Fix overlapping on mobile view
    const modalSidebar = document.querySelector(
      "#pst-primary-sidebar-modal > div.sidebar-primary-items__start.sidebar-primary__section",
    );
    if (modalSidebar) modalSidebar.style.opacity = "0.1";
  }

  /** Collapse the search input, clear results, and restore page opacity. */
  function collapseSearchInput() {
    RESULTS_CONTAINER.style.display = "none";
    SEARCH_INPUT.classList.remove("expanded");
    SEARCH_INPUT.value = "";
    MAIN_PAGE_CONTENT.classList.remove("blurred");
    CURRENT_INDEX = -1;

    const modalSidebar = document.querySelector(
      "#pst-primary-sidebar-modal > div.sidebar-primary-items__start.sidebar-primary__section",
    );
    if (modalSidebar) modalSidebar.style.opacity = "1";
  }

  /** Show a "no results" banner in the results container. */
  function noResultsFoundBanner() {
    RESULTS_CONTAINER.innerHTML = "";
    RESULTS_CONTAINER.style.display = "flex";
    const banner = document.createElement("div");
    banner.className = "warning-banner";
    banner.textContent = "No results found. Press Enter for extended search.";
    banner.style.fontStyle = "italic";
    RESULTS_CONTAINER.appendChild(banner);
  }

  /** Show a transient "Searching…" indicator while Fuse is running. */
  function searchingForResultsBanner() {
    RESULTS_CONTAINER.innerHTML = "";
    RESULTS_CONTAINER.style.display = "flex";
    const banner = document.createElement("div");
    banner.className = "searching-banner";
    banner.textContent = "Searching...";
    banner.style.fontStyle = "italic";
    RESULTS_CONTAINER.appendChild(banner);
  }

  /**
   * Render Fuse results into the dropdown, appending a "Show all results" link.
   * @param {Array} results
   */
  function displayResults(results) {
    RESULTS_CONTAINER.innerHTML = "";
    if (!results.length) return noResultsFoundBanner();

    const fragment = document.createDocumentFragment();
    results.forEach(({ item: { title, text, href } }) => {
      const resultItem = document.createElement("div");
      resultItem.className = "result-item";
      resultItem.dataset.href = href;
      resultItem.addEventListener("click", () => {
        collapseSearchInput();
        navigateToHref(href);
      });

      const resultTitle = document.createElement("div");
      resultTitle.className = "result-title";
      resultTitle.textContent = title;

      const resultText = document.createElement("div");
      resultText.className = "result-text";
      resultText.textContent = truncateTextPreview(text);

      resultItem.append(resultTitle, resultText);
      fragment.appendChild(resultItem);
    });

    // Advanced Search Option
    const query = SEARCH_INPUT.value.trim();
    const advancedSearchItem = document.createElement("div");
    advancedSearchItem.className = "result-item advanced-search";
    advancedSearchItem.style.display = "flex";
    advancedSearchItem.style.justifyContent = "space-between";
    advancedSearchItem.style.alignItems = "center";
    advancedSearchItem.dataset.href = ADVANCE_SEARCH_PATH + "?q=" + query;
    advancedSearchItem.innerHTML = `<a href="${ADVANCE_SEARCH_PATH}?q=${query}">Show all results</a> <span style="font-size: 0.8em; color: gray;">Enter</span>`;
    advancedSearchItem.addEventListener("click", () => {
      window.location.href =
        ADVANCE_SEARCH_PATH + "?q=" + SEARCH_INPUT.value.trim();
    });

    fragment.appendChild(advancedSearchItem);
    RESULTS_CONTAINER.appendChild(fragment);
    RESULTS_CONTAINER.style.display = "flex";
  }

  /**
   * Scroll the currently highlighted result item into view.
   * @param {NodeList} resultsItems
   */
  function focusSelected(resultsItems) {
    if (CURRENT_INDEX >= 0 && CURRENT_INDEX < resultsItems.length) {
      resultsItems.forEach((item) => item.classList.remove("selected"));
      const currentItem = resultsItems[CURRENT_INDEX];
      currentItem.classList.add("selected");
      currentItem.focus();
      currentItem.scrollIntoView({ block: "nearest" });
    }
  }

  /**
   * Handle keyboard navigation: arrows move selection, Enter navigates or opens
   * the advanced search page, Escape collapses.
   * @param {KeyboardEvent} event
   */
  function handleKeyDownSearchInput(event) {
    const resultItems = RESULTS_CONTAINER.querySelectorAll(".result-item");
    switch (event.key) {
      case "Tab":
        event.preventDefault();
        break;
      case "Escape":
        collapseSearchInput();
        break;
      case "Enter":
        event.preventDefault();
        if (CURRENT_INDEX >= 0 && CURRENT_INDEX < resultItems.length) {
          const href = resultItems[CURRENT_INDEX].dataset.href;
          collapseSearchInput();
          navigateToHref(href);
        } else {
          const query = SEARCH_INPUT.value.trim();
          collapseSearchInput();
          window.location.href = ADVANCE_SEARCH_PATH + "?q=" + query;
        }
        break;
      case "ArrowDown":
        if (resultItems.length > 0) {
          CURRENT_INDEX = (CURRENT_INDEX + 1) % resultItems.length;
          focusSelected(resultItems);
        }
        break;
      case "ArrowUp":
        if (resultItems.length > 0) {
          CURRENT_INDEX =
            (CURRENT_INDEX - 1 + resultItems.length) % resultItems.length;
          focusSelected(resultItems);
        }
        break;
      default:
        if (
          event.ctrlKey ||
          event.altKey ||
          event.metaKey ||
          event.key === "Control" ||
          event.key === "Alt"
        ) {
          return;
        }
        if (
          document.documentElement.getAttribute("data-fuse_active") === "true"
        ) {
          searchingForResultsBanner();
        } else {
          RESULTS_CONTAINER.style.display = "none";
        }
        handleSearchInput();
    }
  }

  // 'input' fires after value change, covering keyboard shortcuts and mouse paste.
  function handleInputEvent() {
    if (!SEARCH_INPUT.value.trim()) {
      RESULTS_CONTAINER.style.display = "none";
      return;
    }
    if (document.documentElement.getAttribute("data-fuse_active") === "true") {
      searchingForResultsBanner();
    } else {
      RESULTS_CONTAINER.style.display = "none";
    }
    handleSearchInput();
  }

  const handleSearchInput = debounce(
    () => {
      const query = SEARCH_INPUT.value.trim();
      if (!query) return (RESULTS_CONTAINER.style.display = "none");

      const searchResults = fuseInstance
        .search(query, { limit: parseInt(SEARCH_OPTIONS.limit) })
        .sort((a, b) => {
          const scoreA = (1 - (a.score || 0)) * (a.item.weight || 1);
          const scoreB = (1 - (b.score || 0)) * (b.item.weight || 1);
          return scoreB - scoreA;
        });
      displayResults(searchResults);
    },
    parseInt(SEARCH_OPTIONS.delay) || 300,
  );

  /**
   * Select the correct search bar and results container based on viewport width,
   * then bind input listeners.
   */
  function setupSearchElements() {
    if (window.innerWidth < 1200) {
      SEARCH_BAR = document.querySelector(
        "div.sidebar-header-items__end #search-bar",
      );
      RESULTS_CONTAINER = document.querySelector(
        "div.sidebar-header-items__end .static-search-results",
      );
    } else {
      SEARCH_BAR = document.getElementById("search-bar");
      RESULTS_CONTAINER = document.querySelector(".static-search-results");
    }
    if (!SEARCH_BAR) {
      console.warn("SEARCH_BAR not found for current view.");
      return;
    }
    SEARCH_INPUT = SEARCH_BAR.querySelector(".bd-search input.form-control");
    if (SEARCH_INPUT) {
      SEARCH_INPUT.addEventListener("click", expandSearchInput);
      SEARCH_INPUT.addEventListener("keydown", handleKeyDownSearchInput);
      SEARCH_INPUT.addEventListener("input", handleInputEvent);
    }
  }

  /**
   * Global shortcut handler: Escape collapses, Ctrl+K expands.
   * @param {KeyboardEvent} event
   */
  function handleGlobalKeyDown(event) {
    if (event.key === "Escape") collapseSearchInput();
    else if (event.key === "k" && event.ctrlKey) expandSearchInput();
  }

  /**
   * Collapse the search UI when the user clicks outside it.
   * @param {MouseEvent} event
   */
  function handleGlobalClick(event) {
    if (
      !RESULTS_CONTAINER.contains(event.target) &&
      event.target !== SEARCH_INPUT
    ) {
      collapseSearchInput();
    }
  }

  /**
   * Create the Fuse instance and mark the page as search-ready.
   * @param {Array} data
   * @param {Object} options
   */
  function initializeFuse(data, options) {
    fuseInstance = new Fuse(data, options);
    document.documentElement.setAttribute("data-fuse_active", "true");
  }

  // Initialize search functionality on page load
  setupSearchElements();
  window.addEventListener("resize", debounce(setupSearchElements, 250));
  document.addEventListener("keydown", handleGlobalKeyDown);
  document.addEventListener("click", handleGlobalClick);

  fetch(SEARCH_FILE)
    .then((response) => {
      if (!response.ok)
        throw new Error(`[AST]: HTTPS error ${response.statusText}`);
      return response.json();
    })
    .then((SEARCH_DATA) => initializeFuse(SEARCH_DATA, SEARCH_OPTIONS))
    .catch((error) =>
      console.error(`[AST]: Cannot fetch ${SEARCH_FILE}`, error.message),
    );
});
