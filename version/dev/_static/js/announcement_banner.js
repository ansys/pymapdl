/**
 * announcement_banner.js
 *
 * Handles the announcement banner and modal, including:
 * - Dismissal state (localStorage)
 * - Fetching announcement.html for extra notifications
 * - Building notification cards from ast config and announcement.html
 * - Aligning banner to middle column width
 * - Modal open/close behavior
 *
 * This file is included in the theme's static files and is loaded on every page.
 */

document.addEventListener("DOMContentLoaded", function () {
  const wrap = document.querySelector(".ast-announcement-wrap");
  const closeBtn = document.getElementById("ast-announcement-close");

  /**
   * Function to compute a hash of the banner content for localStorage key.
   * Uses SHA-1 if available, otherwise falls back to a simple hash.
   *
   * @param {string} str - The string to hash
   * @returns {string} - The hex hash of the string
   */
  function hashTextFallback(str) {
    var h = 5381;
    for (var i = 0; i < str.length; i++) {
      h = ((h << 5) + h) ^ str.charCodeAt(i);
    }
    return (h >>> 0).toString(16);
  }

  /**
   *
   * @param {string} str - string to hash
   * @returns {Promise<string>} - hex hash
   */
  async function hashText(str) {
    try {
      const buf = await crypto.subtle.digest(
        "SHA-1",
        new TextEncoder().encode(str),
      );
      return Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, "0"))
        .join("")
        .slice(0, 16);
    } catch (e) {
      return hashTextFallback(str);
    }
  }

  // Called after all banner content is known (ast_items + fetched announcement.html)
  /**
   * Function to apply dismissal state based on content hash.
   * @param {string} contentKey - The content key to hash and check dismissal state
   */
  function applyDismiss(contentKey) {
    hashText(contentKey).then(function (hash) {
      const STORAGE_KEY = "ast-announcement-dismissed:" + hash;
      if (wrap && localStorage.getItem(STORAGE_KEY) === "1") {
        wrap.setAttribute("hidden", "");
        return;
      }
      if (closeBtn && wrap) {
        closeBtn.addEventListener(
          "click",
          function () {
            wrap.setAttribute("hidden", "");
            localStorage.setItem(STORAGE_KEY, "1");
          },
          { once: true },
        );
      }
    });
  }

  // Size banner to 80% of .bd-content (middle column, adapts to sidebar presence)
  /**
   * Function to align the announcement banner to 80% of the middle column width.
   * This is called on initial load and on window resize.
   */
  function alignToBdArticle() {
    const content = document.querySelector(".bd-main .bd-content");
    if (content && wrap) {
      wrap.style.width = content.getBoundingClientRect().width * 0.8 + "px";
      wrap.style.marginLeft = "auto";
      wrap.style.marginRight = "auto";
    }
  }
  // Defer initial alignment until after layout is complete
  if (wrap && !wrap.hasAttribute("hidden")) {
    requestAnimationFrame(alignToBdArticle);
  }
  window.addEventListener("resize", alignToBdArticle);

  const ATTENTION_TYPES = ["warning", "error"];

  /**
   * Function to detect the type of notification based on the background color of an element.
   * @param {HTMLElement} el - The element to detect the type from
   * @returns {string} - The detected type ("success", "warning", "info", etc.)
   */
  function detectType(el) {
    const rgb = el.style.backgroundColor || "";
    const match = rgb.match(/\d+/g);
    if (match) {
      const [r, g, b] = match.map(Number);
      if (g > r && g > b) return "success";
      if (r > g && r > b) return "warning";
      if (b > r && b > g) return "info";
    }
    return "info";
  }

  /**
   * Function to create a notification card element.
   * @param {string} type - The type of notification ("success", "warning", "info", etc.)
   * @param {string} html - The HTML content of the notification
   * @param {string} link - The URL for the "Learn more" link (optional)
   * @returns {HTMLElement} - The constructed notification card element
   */
  function makeCard(type, html, link) {
    const card = document.createElement("div");
    card.classList.add("ast-notification-card", "ast-notification-" + type);
    const iconEl = document.createElement("span");
    iconEl.classList.add("ast-notification-icon");
    // icon rendered via CSS ::before using FontAwesome
    const body = document.createElement("div");
    body.classList.add("ast-notification-body");
    body.innerHTML = html;
    if (link) {
      const a = document.createElement("a");
      a.href = link;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.classList.add("ast-notification-link");
      a.textContent = "Learn more \u2192";
      body.appendChild(a);
    }
    card.appendChild(iconEl);
    card.appendChild(body);
    return card;
  }

  /**
   * Function to build the notifications section in the modal.
   * @param {Array} extraItems - Array of extra notification items from announcement.html
   */
  function buildNotifications(extraItems) {
    // extraItems: array of {type, html} from announcement.html
    const modalBody = document.querySelector(".ast-announcement-modal-body");
    if (!modalBody) return;
    modalBody.innerHTML = "";

    // Parse ast items from JSON data attribute
    let astItems = [];
    try {
      astItems = JSON.parse(modalBody.dataset.astItems || "[]");
    } catch (e) {}

    const section = document.createElement("div");
    section.classList.add("ast-announcement-extra");

    const heading = document.createElement("div");
    heading.classList.add("ast-notification-heading");
    heading.textContent = "Notifications";
    section.appendChild(heading);

    // Cards from announcement_banner config (one or many)
    astItems.forEach(function (item) {
      section.appendChild(
        makeCard(
          item.type || "info",
          item.message || "",
          item.link || item.url || "",
        ),
      );
    });

    // Cards from announcement.html (if any)
    extraItems.forEach(function (item) {
      section.appendChild(makeCard(item.type, item.html, ""));
    });

    modalBody.appendChild(section);

    // Update banner text + button based on notification count
    const btnEl = document.getElementById("ast-announcement-details-btn");
    const textEl = document.getElementById("ast-announcement-text");
    const total = astItems.length + extraItems.length;
    const astUrl =
      astItems.length === 1 && (astItems[0].url || astItems[0].link)
        ? astItems[0].url || astItems[0].link
        : "";
    const attention =
      astItems.filter(function (i) {
        return ATTENTION_TYPES.includes(i.type);
      }).length +
      extraItems.filter(function (i) {
        return ATTENTION_TYPES.includes(i.type);
      }).length;

    if (btnEl) {
      if (total === 1) {
        // Single announcement_banner with a url: direct link button
        if (astUrl) {
          btnEl.href = astUrl;
          btnEl.target = "_blank";
          btnEl.rel = "noopener noreferrer";
          btnEl.removeAttribute("data-modal");
          btnEl.style.display = "";
        } else {
          btnEl.style.display = "none";
        }
      } else {
        // Multiple notifications: update banner text + show popup button
        if (textEl) {
          let summary =
            "There are " + total + " notification" + (total !== 1 ? "s" : "");
          if (attention > 0) {
            summary +=
              " \u2014 " +
              attention +
              " require" +
              (attention !== 1 ? "" : "s") +
              " attention";
          }
          textEl.textContent = summary;
        }
        btnEl.removeAttribute("href");
        btnEl.setAttribute("data-modal", "true");
        btnEl.style.display = "";
        let countLabel = total + " notification" + (total !== 1 ? "s" : "");
        if (attention > 0) {
          countLabel +=
            " \u2014 " +
            attention +
            " require" +
            (attention !== 1 ? "" : "s") +
            " attention";
        }
        btnEl.setAttribute("title", countLabel);
        btnEl.setAttribute("aria-label", countLabel);
      }
    }
  }

  // Resolve the base URL from the script tag's data-base-url attribute
  // (Jinja's pathto() is only available in .html templates, not static .js files)
  const scriptEl =
    document.currentScript || document.querySelector("script[data-base-url]");
  const baseUrl = (scriptEl && scriptEl.dataset.baseUrl) || "";

  // Fetch announcement.html then build notifications
  /**
   * Fetches the announcement.html file and builds notifications based on its content.
   * If announcement.html is not found or empty, it will still build notifications from ast config.
   * After building notifications, it applies dismissal state based on the combined content.
   */
  fetch(baseUrl + "announcement.html")
    .then(function (response) {
      if (!response.ok) {
        return null;
      }
      return response.text();
    })
    .then(function (text) {
      const extraItems = [];
      if (text && text.trim()) {
        const parser = document.createElement("div");
        parser.innerHTML = text;
        parser.querySelectorAll("p").forEach(function (p) {
          const type = detectType(p);
          p.style.backgroundColor = "";
          p.style.padding = "";
          p.style.width = "";
          extraItems.push({ type: type, html: p.innerHTML });
        });
      }

      // If no ast config items but announcement.html has content:
      // derive banner type from fetched items and show the wrap
      const modalBody = document.querySelector(".ast-announcement-modal-body");
      let astItems = [];
      try {
        astItems = JSON.parse(
          (modalBody && modalBody.dataset.astItems) || "[]",
        );
      } catch (e) {}

      if (astItems.length === 0 && extraItems.length > 0) {
        const PRIORITY = { error: 3, warning: 2, success: 1, info: 0 };
        let dominant = "info";
        extraItems.forEach(function (i) {
          if ((PRIORITY[i.type] || 0) > (PRIORITY[dominant] || 0))
            dominant = i.type;
        });
        // Apply dominant type class to banner and modal
        const banner = document.querySelector(".ast-announcement");
        const modal = document.querySelector(".ast-announcement-modal");
        ["info", "warning", "error", "success"].forEach(function (t) {
          if (banner) banner.classList.remove(t);
          if (modal) modal.classList.remove(t);
        });
        if (banner) banner.classList.add(dominant);
        if (modal) modal.classList.add(dominant);

        // Set initial banner text from first extraItem
        const textEl = document.getElementById("ast-announcement-text");
        if (textEl && extraItems.length === 1) {
          textEl.innerHTML = extraItems[0].html;
        }

        if (wrap) {
          wrap.removeAttribute("hidden");
          // Re-run alignment now that the wrap is visible
          alignToBdArticle();
        }
      }

      buildNotifications(extraItems);

      // Compute dismiss key from all known content (ast_items + fetched items)
      const allContent =
        astItems
          .map(function (i) {
            return i.message || "";
          })
          .join("|") +
        "|" +
        extraItems
          .map(function (i) {
            return i.html || "";
          })
          .join("|");
      applyDismiss(allContent);
    })
    .catch(function () {
      buildNotifications([]);
      applyDismiss("");
    });

  // Modal open/close
  const detailsBtn = document.getElementById("ast-announcement-details-btn");
  const overlay = document.getElementById("ast-announcement-overlay");
  const modalClose = document.getElementById("ast-announcement-modal-close");

  if (detailsBtn && overlay) {
    detailsBtn.addEventListener("click", function (e) {
      if (!detailsBtn.dataset.modal) return; // plain link — let browser handle it
      e.preventDefault();
      overlay.classList.add("visible");
    });

    modalClose.addEventListener("click", function () {
      overlay.classList.remove("visible");
    });

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) {
        overlay.classList.remove("visible");
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        overlay.classList.remove("visible");
      }
    });
  }
});
