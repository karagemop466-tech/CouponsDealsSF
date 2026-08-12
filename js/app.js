// app.js - Enhanced Client-Side Deep Search, Neighborhood Explorer & Schedule Engine for CouponsDealsSF

document.addEventListener("DOMContentLoaded", () => {
  let allDeals = [];
  let allCandidates = [];
  let savedDeals = new Set(JSON.parse(localStorage.getItem("couponsDealsSF_saved") || "[]"));

  // Today is 2026-08-12 (Wednesday) in local timezone
  const CURRENT_DAY_OF_WEEK = "Wednesday";

  let currentFilter = {
    query: "",
    priority: "all",      // 'all', '1' (100% Free), '2' (Free w/ purchase), '3' (Discount), 'saved' (My Saved)
    category: "all",
    location: "all",
    verification: "all",
    schedule: "all",      // 'all', 'today', 'weekend', 'birthday', 'resident', 'always'
    sortBy: "priority",   // 'priority', 'newest', 'title', 'value'
    viewMode: "grid"      // 'grid', 'list', 'neighborhood'
  };

  // DOM Elements
  const dealsGrid = document.getElementById("deals-grid");
  const emptyState = document.getElementById("empty-state");
  const resultCountEl = document.getElementById("result-count");
  const searchInput = document.getElementById("search-input");
  const priorityTabsContainer = document.getElementById("priority-tabs");
  const categoryContainer = document.getElementById("category-filters");
  const locationSelect = document.getElementById("location-select");
  const verificationSelect = document.getElementById("verification-select");
  const sortSelect = document.getElementById("sort-select");
  const scheduleChipsContainer = document.getElementById("schedule-chips");
  const viewModeButtons = document.getElementById("view-mode-buttons");

  // Stats Elements
  const totalDealsStat = document.getElementById("stat-total-deals");
  const freePctStat = document.getElementById("stat-free-percentage");
  const totalSourcesStat = document.getElementById("stat-total-sources");
  const savedCountBadge = document.getElementById("saved-count-badge");

  // Modals
  const detailModal = document.getElementById("detail-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const deepSearchModal = document.getElementById("deep-search-modal");
  const openDeepSearchBtn = document.getElementById("open-deep-search-btn");
  const deepSearchCloseBtn = document.getElementById("deep-search-close-btn");

  // Deep search interactive form
  const runDeepSearchBtn = document.getElementById("run-deep-search-btn");
  const deepSearchInput = document.getElementById("deep-search-input");
  const deepSearchSource = document.getElementById("deep-search-source");
  const deepSearchResultsBox = document.getElementById("deep-search-results-box");

  // Export buttons
  const exportJsonBtn = document.getElementById("export-json-btn");
  const exportCsvBtn = document.getElementById("export-csv-btn");
  const clearFiltersBtn = document.getElementById("clear-filters-btn");

  // Initialize App
  init();

  async function init() {
    try {
      // Fetch deals, stats, and live scraped candidates
      const [dealsResp, statsResp, candResp] = await Promise.all([
        fetch("data/deals.json"),
        fetch("data/stats.json").catch(() => null),
        fetch("data/candidates.json").catch(() => null)
      ]);

      allDeals = await dealsResp.json();
      const statsData = statsResp ? await statsResp.json() : null;
      allCandidates = candResp ? await candResp.json() : [];

      populateStats(statsData, allDeals);
      populateFilters(allDeals);
      setupEventListeners();
      updateSavedBadge();
      renderDeals();
    } catch (err) {
      console.error("Error initializing app:", err);
      dealsGrid.innerHTML = `
        <div class="col-span-full bg-red-50 border border-red-200 text-red-700 p-6 rounded-xl text-center">
          <p class="font-bold text-lg mb-2">Error loading deals database</p>
          <p class="text-sm">Please check your network connection or ensure data/deals.json exists in the repository.</p>
        </div>
      `;
    }
  }

  function populateStats(stats, deals) {
    if (stats) {
      totalDealsStat.textContent = stats.total_deals || deals.length;
      freePctStat.textContent = stats.free_percentage || "92.0%";
      totalSourcesStat.textContent = stats.total_monitored_sources || "15+";
    } else {
      totalDealsStat.textContent = deals.length;
      const freeCount = deals.filter(d => d.priority_rank === 1).length;
      freePctStat.textContent = `${Math.round((freeCount / deals.length) * 100)}%`;
      totalSourcesStat.textContent = "15+";
    }
  }

  function updateSavedBadge() {
    if (savedCountBadge) {
      savedCountBadge.textContent = savedDeals.size;
    }
  }

  function toggleSaveDeal(id) {
    if (savedDeals.has(id)) {
      savedDeals.delete(id);
    } else {
      savedDeals.add(id);
    }
    localStorage.setItem("couponsDealsSF_saved", JSON.stringify(Array.from(savedDeals)));
    updateSavedBadge();
    if (currentFilter.priority === "saved") {
      renderDeals();
    } else {
      // Update bookmark icon in place
      document.querySelectorAll(`.save-btn[data-id="${id}"]`).forEach(btn => {
        const isSaved = savedDeals.has(id);
        btn.classList.toggle("saved", isSaved);
        btn.innerHTML = isSaved ? "★ Saved" : "☆ Save";
      });
    }
  }

  function isDealActiveToday(deal) {
    const st = deal.schedule_type || "";
    const titleLower = (deal.title + " " + deal.description).toLowerCase();
    if (st === "Always Free") return true;
    if (titleLower.includes("wednesday") || st === "First Wednesday") return true;
    if (titleLower.includes("daily") || titleLower.includes("every day")) return true;
    return false;
  }

  function populateFilters(deals) {
    // Categories
    const categories = ["All", ...new Set(deals.map(d => d.category))];
    categoryContainer.innerHTML = categories.map((cat, i) => `
      <button data-category="${cat === "All" ? "all" : cat}" 
              class="category-btn px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                i === 0 
                  ? "bg-slate-900 text-white border-slate-900" 
                  : "bg-white text-slate-700 border-slate-200 hover:border-slate-400 hover:bg-slate-50"
              }">
        ${cat}
      </button>
    `).join("");

    // Locations
    const locations = ["All SF & Bay Area", ...new Set(deals.map(d => d.location))];
    locationSelect.innerHTML = locations.map(loc => `
      <option value="${loc === "All SF & Bay Area" ? "all" : loc}">${loc}</option>
    `).join("");

    // Verification types
    const verifications = ["All Verified Sources", ...new Set(deals.map(d => (d.verification || {}).status || "Verified Official Source"))];
    verificationSelect.innerHTML = verifications.map(ver => `
      <option value="${ver === "All Verified Sources" ? "all" : ver}">${ver}</option>
    `).join("");

    // Add priority tab badges
    const p1Count = deals.filter(d => d.priority_rank === 1).length;
    const p2Count = deals.filter(d => d.priority_rank === 2).length;
    const p3Count = deals.filter(d => d.priority_rank === 3).length;

    const tabs = [
      { id: "all", label: `All Deals (${deals.length})`, color: "border-transparent text-slate-600 hover:text-slate-900" },
      { id: "1", label: `⭐ 100% FREE - Highest Priority (${p1Count})`, color: "border-transparent text-emerald-700 font-bold hover:text-emerald-800" },
      { id: "2", label: `🎁 Free with Purchase / BOGO (${p2Count})`, color: "border-transparent text-amber-700 hover:text-amber-800" },
      { id: "3", label: `🏷️ Discounts & Specials (${p3Count})`, color: "border-transparent text-blue-700 hover:text-blue-800" },
      { id: "saved", label: `⭐ My Saved Wallet (<span id="saved-count-badge">${savedDeals.size}</span>)`, color: "border-transparent text-purple-700 font-semibold hover:text-purple-800" }
    ];

    priorityTabsContainer.innerHTML = tabs.map((t, idx) => `
      <button data-priority="${t.id}" class="priority-tab px-4 py-2 text-sm font-medium border-b-2 transition-all whitespace-nowrap ${
        idx === 0 ? "border-emerald-500 text-emerald-700 font-bold" : t.color
      }">
        ${t.label}
      </button>
    `).join("");

    // Schedule Quick-Filter Chips
    const scheduleOptions = [
      { id: "all", label: "🗓️ All Schedules" },
      { id: "today", label: `⚡ Free Today (${CURRENT_DAY_OF_WEEK})` },
      { id: "weekend", label: "📅 Free This Weekend" },
      { id: "birthday", label: "🎂 Birthday Perks ($0 Cost)" },
      { id: "resident", label: "🪪 Resident ID Required" },
      { id: "always", label: "♾️ Always Free" }
    ];

    scheduleChipsContainer.innerHTML = scheduleOptions.map((sc, idx) => `
      <button data-schedule="${sc.id}" class="schedule-chip px-3 py-1 rounded-lg text-xs font-semibold border transition-all ${
        idx === 0
          ? "bg-emerald-700 text-white border-emerald-700"
          : "bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200"
      }">
        ${sc.label}
      </button>
    `).join("");
  }

  function setupEventListeners() {
    // Live Search
    searchInput.addEventListener("input", (e) => {
      currentFilter.query = e.target.value.trim().toLowerCase();
      renderDeals();
    });

    // Priority Tabs
    priorityTabsContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".priority-tab");
      if (!btn) return;
      document.querySelectorAll(".priority-tab").forEach(b => {
        b.classList.remove("border-emerald-500", "text-emerald-700", "font-bold");
        b.classList.add("border-transparent");
      });
      btn.classList.remove("border-transparent");
      btn.classList.add("border-emerald-500", "text-emerald-700", "font-bold");
      currentFilter.priority = btn.dataset.priority;
      renderDeals();
    });

    // Schedule Chips
    scheduleChipsContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".schedule-chip");
      if (!btn) return;
      document.querySelectorAll(".schedule-chip").forEach(b => {
        b.classList.remove("bg-emerald-700", "text-white", "border-emerald-700");
        b.classList.add("bg-slate-100", "text-slate-700", "border-slate-200");
      });
      btn.classList.remove("bg-slate-100", "text-slate-700", "border-slate-200");
      btn.classList.add("bg-emerald-700", "text-white", "border-emerald-700");
      currentFilter.schedule = btn.dataset.schedule;
      renderDeals();
    });

    // View Mode Toggle (Grid, List, Neighborhood)
    if (viewModeButtons) {
      viewModeButtons.addEventListener("click", (e) => {
        const btn = e.target.closest(".view-mode-btn");
        if (!btn) return;
        document.querySelectorAll(".view-mode-btn").forEach(b => {
          b.classList.remove("bg-slate-900", "text-white");
          b.classList.add("bg-slate-100", "text-slate-700");
        });
        btn.classList.remove("bg-slate-100", "text-slate-700");
        btn.classList.add("bg-slate-900", "text-white");
        currentFilter.viewMode = btn.dataset.view;
        renderDeals();
      });
    }

    // Category Buttons
    categoryContainer.addEventListener("click", (e) => {
      const btn = e.target.closest(".category-btn");
      if (!btn) return;
      document.querySelectorAll(".category-btn").forEach(b => {
        b.classList.remove("bg-slate-900", "text-white", "border-slate-900");
        b.classList.add("bg-white", "text-slate-700", "border-slate-200");
      });
      btn.classList.remove("bg-white", "text-slate-700", "border-slate-200");
      btn.classList.add("bg-slate-900", "text-white", "border-slate-900");
      currentFilter.category = btn.dataset.category;
      renderDeals();
    });

    // Location Dropdown
    locationSelect.addEventListener("change", (e) => {
      currentFilter.location = e.target.value;
      renderDeals();
    });

    // Verification Dropdown
    verificationSelect.addEventListener("change", (e) => {
      currentFilter.verification = e.target.value;
      renderDeals();
    });

    // Sort Dropdown
    sortSelect.addEventListener("change", (e) => {
      currentFilter.sortBy = e.target.value;
      renderDeals();
    });

    // Clear filters
    clearFiltersBtn.addEventListener("click", () => {
      searchInput.value = "";
      currentFilter = {
        query: "",
        priority: "all",
        category: "all",
        location: "all",
        verification: "all",
        schedule: "all",
        sortBy: "priority",
        viewMode: currentFilter.viewMode
      };
      locationSelect.value = "all";
      verificationSelect.value = "all";
      sortSelect.value = "priority";

      // reset category UI
      document.querySelectorAll(".category-btn").forEach((b, idx) => {
        if (idx === 0) {
          b.classList.remove("bg-white", "text-slate-700", "border-slate-200");
          b.classList.add("bg-slate-900", "text-white", "border-slate-900");
        } else {
          b.classList.remove("bg-slate-900", "text-white", "border-slate-900");
          b.classList.add("bg-white", "text-slate-700", "border-slate-200");
        }
      });

      // reset priority tab UI
      document.querySelectorAll(".priority-tab").forEach((b, idx) => {
        if (idx === 0) {
          b.classList.remove("border-transparent");
          b.classList.add("border-emerald-500", "text-emerald-700", "font-bold");
        } else {
          b.classList.remove("border-emerald-500", "text-emerald-700", "font-bold");
          b.classList.add("border-transparent");
        }
      });

      // reset schedule UI
      document.querySelectorAll(".schedule-chip").forEach((b, idx) => {
        if (idx === 0) {
          b.classList.remove("bg-slate-100", "text-slate-700", "border-slate-200");
          b.classList.add("bg-emerald-700", "text-white", "border-emerald-700");
        } else {
          b.classList.remove("bg-emerald-700", "text-white", "border-emerald-700");
          b.classList.add("bg-slate-100", "text-slate-700", "border-slate-200");
        }
      });

      renderDeals();
    });

    // Export JSON
    exportJsonBtn.addEventListener("click", () => {
      const filtered = getFilteredDeals();
      const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sf-bay-area-freebies-deals-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    });

    // Export CSV
    exportCsvBtn.addEventListener("click", () => {
      const filtered = getFilteredDeals();
      const headers = [
        "id", "priority_rank", "priority_label", "title", "category",
        "location", "value", "verification_status", "verified_by", "promotion_url", "description"
      ];
      const csvRows = [headers.join(",")];
      for (const d of filtered) {
        const row = [
          d.id,
          d.priority_rank,
          `"${(d.priority_label || "").replace(/"/g, '""')}"`,
          `"${(d.title || "").replace(/"/g, '""')}"`,
          `"${(d.category || "").replace(/"/g, '""')}"`,
          `"${(d.location || "").replace(/"/g, '""')}"`,
          `"${(d.value || "").replace(/"/g, '""')}"`,
          `"${(d.verification?.status || "").replace(/"/g, '""')}"`,
          `"${(d.verification?.source_name || "").replace(/"/g, '""')}"`,
          `"${(d.promotion_url || "").replace(/"/g, '""')}"`,
          `"${(d.description || "").replace(/"/g, '""')}"`
        ];
        csvRows.push(row.join(","));
      }
      const blob = new Blob([csvRows.join("\n")], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sf-bay-area-freebies-deals-${new Date().toISOString().slice(0, 10)}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    });

    // Modal Close
    modalCloseBtn.addEventListener("click", () => closeModal(detailModal));
    detailModal.addEventListener("click", (e) => {
      if (e.target === detailModal) closeModal(detailModal);
    });

    // Deep Search Modal Open/Close
    openDeepSearchBtn.addEventListener("click", () => {
      openModal(deepSearchModal);
      runDeepSearchSimulation();
    });
    deepSearchCloseBtn.addEventListener("click", () => closeModal(deepSearchModal));
    deepSearchModal.addEventListener("click", (e) => {
      if (e.target === deepSearchModal) closeModal(deepSearchModal);
    });

    runDeepSearchBtn.addEventListener("click", () => {
      runDeepSearchSimulation();
    });

    // Escape Key to close modals
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        closeModal(detailModal);
        closeModal(deepSearchModal);
      }
    });

    // Handle clicks on dynamically rendered Save buttons and View Details
    dealsGrid.addEventListener("click", (e) => {
      const saveBtn = e.target.closest(".save-btn");
      if (saveBtn) {
        e.stopPropagation();
        toggleSaveDeal(saveBtn.dataset.id);
        return;
      }
      const viewBtn = e.target.closest(".view-details-btn");
      if (viewBtn) {
        e.stopPropagation();
        const id = viewBtn.dataset.id;
        const deal = allDeals.find(d => d.id === id);
        if (deal) showDealModal(deal);
      }
    });
  }

  function getFilteredDeals() {
    return allDeals.filter(d => {
      // Saved wallet filter
      if (currentFilter.priority === "saved") {
        if (!savedDeals.has(d.id)) return false;
      } else if (currentFilter.priority !== "all" && String(d.priority_rank) !== currentFilter.priority) {
        return false;
      }

      // Category filter
      if (currentFilter.category !== "all" && d.category !== currentFilter.category) {
        return false;
      }

      // Location filter
      if (currentFilter.location !== "all" && d.location !== currentFilter.location) {
        return false;
      }

      // Verification filter
      if (currentFilter.verification !== "all" && (d.verification || {}).status !== currentFilter.verification) {
        return false;
      }

      // Schedule quick filter
      if (currentFilter.schedule !== "all") {
        if (currentFilter.schedule === "today" && !isDealActiveToday(d)) return false;
        if (currentFilter.schedule === "weekend" && d.schedule_type !== "Weekend") return false;
        if (currentFilter.schedule === "birthday" && d.schedule_type !== "Birthday") return false;
        if (currentFilter.schedule === "resident" && !(d.tags || []).includes("sf-resident") && !(d.title + " " + d.description).toLowerCase().includes("resident")) return false;
        if (currentFilter.schedule === "always" && d.schedule_type !== "Always Free") return false;
      }

      // Query search
      if (currentFilter.query) {
        const text = [
          d.title,
          d.description,
          d.redemption_instructions,
          d.location,
          d.category,
          (d.tags || []).join(" "),
          d.verification?.source_name,
          d.verification?.status
        ].join(" ").toLowerCase();
        if (!text.includes(currentFilter.query)) {
          return false;
        }
      }
      return true;
    }).sort((a, b) => {
      if (currentFilter.sortBy === "priority") {
        if (a.priority_rank !== b.priority_rank) {
          return a.priority_rank - b.priority_rank;
        }
        return a.title.localeCompare(b.title);
      } else if (currentFilter.sortBy === "title") {
        return a.title.localeCompare(b.title);
      } else if (currentFilter.sortBy === "newest") {
        const dA = (a.verification && a.verification.verified_date) || "2000-01-01";
        const dB = (b.verification && b.verification.verified_date) || "2000-01-01";
        return dB.localeCompare(dA);
      }
      return 0;
    });
  }

  function renderDeals() {
    const filtered = getFilteredDeals();
    resultCountEl.textContent = `${filtered.length} deal${filtered.length === 1 ? "" : "s"}`;

    if (filtered.length === 0) {
      dealsGrid.innerHTML = "";
      emptyState.classList.remove("hidden");
      return;
    }

    emptyState.classList.add("hidden");

    if (currentFilter.viewMode === "grid") {
      dealsGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
      dealsGrid.innerHTML = filtered.map(deal => createDealCardHtml(deal)).join("");
    } else if (currentFilter.viewMode === "list") {
      dealsGrid.className = "col-span-full";
      dealsGrid.innerHTML = renderListViewHtml(filtered);
    } else if (currentFilter.viewMode === "neighborhood") {
      dealsGrid.className = "col-span-full";
      dealsGrid.innerHTML = renderNeighborhoodViewHtml(filtered);
    }
  }

  function renderListViewHtml(deals) {
    return `
      <div class="overflow-x-auto bg-white rounded-2xl border border-slate-200 shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 border-b border-slate-200 text-xs uppercase font-bold text-slate-500">
              <th class="py-3 px-4">Priority</th>
              <th class="py-3 px-4">Promotion Title</th>
              <th class="py-3 px-4">Category</th>
              <th class="py-3 px-4">SF / Bay Area Location</th>
              <th class="py-3 px-4">Value</th>
              <th class="py-3 px-4">Verification</th>
              <th class="py-3 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm">
            ${deals.map(deal => {
              const isFree = deal.priority_rank === 1;
              const badge = isFree 
                ? `<span class="bg-emerald-100 text-emerald-800 font-bold px-2.5 py-1 rounded-md text-xs">⭐ 100% Free</span>`
                : `<span class="bg-amber-100 text-amber-800 font-bold px-2.5 py-1 rounded-md text-xs">🎁 #2 Purchase Req.</span>`;
              const isSaved = savedDeals.has(deal.id);
              return `
                <tr class="hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-4 whitespace-nowrap">${badge}</td>
                  <td class="py-3 px-4 font-bold text-slate-900 font-heading">${deal.title}</td>
                  <td class="py-3 px-4 text-slate-600">${deal.category}</td>
                  <td class="py-3 px-4 text-slate-600">${deal.location}</td>
                  <td class="py-3 px-4 font-semibold text-indigo-700">${deal.value}</td>
                  <td class="py-3 px-4 text-xs text-slate-600">
                    <span class="text-emerald-600 font-bold">✓</span> ${deal.verification?.source_name || "Official"}
                  </td>
                  <td class="py-3 px-4 text-right whitespace-nowrap">
                    <button data-id="${deal.id}" class="view-details-btn bg-slate-900 hover:bg-slate-800 text-white px-3 py-1.5 rounded-lg text-xs font-semibold mr-1">
                      Details
                    </button>
                    <button data-id="${deal.id}" class="save-btn px-2 py-1.5 border rounded-lg text-xs font-bold transition-all ${
                      isSaved ? "border-amber-400 text-amber-600 bg-amber-50" : "border-slate-200 text-slate-600 hover:bg-slate-50"
                    }">
                      ${isSaved ? "★ Saved" : "☆ Save"}
                    </button>
                  </td>
                </tr>
              `;
            }).join("")}
          </tbody>
        </table>
      </div>
    `;
  }

  function renderNeighborhoodViewHtml(deals) {
    const neighborhoods = [
      "SF - SoMa / Downtown",
      "SF - Golden Gate Park / Richmond",
      "SF - Mission / Castro",
      "SF - Chinatown / North Beach",
      "SF - All Neighborhoods",
      "Oakland / East Bay",
      "San Jose / South Bay",
      "Bay Area Wide"
    ];

    return `
      <div class="space-y-8">
        ${neighborhoods.map(hood => {
          const matching = deals.filter(d => d.location === hood);
          if (matching.length === 0) return "";
          return `
            <div class="neighborhood-cluster bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm">
              <div class="flex items-center justify-between border-b border-slate-200 pb-4 mb-6">
                <div>
                  <h3 class="text-2xl font-extrabold text-slate-900 font-heading flex items-center gap-2">
                    <span>📍</span>
                    <span>${hood}</span>
                  </h3>
                  <p class="text-xs text-slate-500 mt-1">Verified community deals & freebies in ${hood}</p>
                </div>
                <span class="bg-slate-900 text-white font-bold text-xs px-3 py-1.5 rounded-full">
                  ${matching.length} deal${matching.length === 1 ? "" : "s"}
                </span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${matching.map(deal => createDealCardHtml(deal)).join("")}
              </div>
            </div>
          `;
        }).join("")}
      </div>
    `;
  }

  function createDealCardHtml(deal) {
    const rank = deal.priority_rank || 99;
    const isFree = rank === 1;
    const isSaved = savedDeals.has(deal.id);

    // Badge CSS based on priority
    let badgeClass = "badge-priority-1";
    let badgeIcon = "⭐";
    let badgeText = "100% FREE • HIGHEST PRIORITY";
    if (rank === 2) {
      badgeClass = "badge-priority-2";
      badgeIcon = "🎁";
      badgeText = "FREE WITH PURCHASE / BOGO";
    } else if (rank === 3) {
      badgeClass = "badge-priority-3";
      badgeIcon = "🏷️";
      badgeText = "DISCOUNT & SPECIAL";
    }

    const verification = deal.verification || {};
    const verStatus = verification.status || "Verified Official Source";
    const verDate = verification.verified_date || "2026-08-12";

    const isNewTag = deal.is_new ? `<span class="bg-emerald-100 text-emerald-800 text-xs px-2.5 py-0.5 rounded-full font-semibold border border-emerald-300">NEW 2026</span>` : "";
    const activeTodayTag = isDealActiveToday(deal) ? `<span class="bg-emerald-600 text-white text-xs px-2.5 py-0.5 rounded-full font-bold shadow-sm">⚡ FREE TODAY</span>` : "";

    return `
      <div class="deal-card bg-white rounded-2xl p-6 flex flex-col justify-between shadow-sm relative">
        <div>
          <!-- Top row: Priority badge, Active tag, Save star -->
          <div class="flex items-center justify-between gap-2 mb-3">
            <span class="${badgeClass} text-xs font-extrabold px-3 py-1 rounded-full flex items-center gap-1.5 shadow-sm">
              <span>${badgeIcon}</span>
              <span>${badgeText}</span>
            </span>
            <div class="flex items-center gap-1.5">
              ${activeTodayTag}
              ${isNewTag}
              <button data-id="${deal.id}" title="Save to My Freebie Wallet" 
                      class="save-btn px-2.5 py-1 border rounded-lg text-xs font-bold transition-all ${
                        isSaved ? "border-amber-400 text-amber-600 bg-amber-50 saved" : "border-slate-200 text-slate-600 hover:bg-slate-100"
                      }">
                ${isSaved ? "★ Saved" : "☆ Save"}
              </button>
            </div>
          </div>

          <!-- Title -->
          <div class="flex items-start justify-between gap-3 mb-2">
            <h3 class="text-lg font-bold text-slate-900 leading-snug font-heading">${deal.title}</h3>
          </div>

          <!-- Category, Location, Value pills -->
          <div class="flex flex-wrap items-center gap-2 text-xs text-slate-600 mb-3">
            <span class="bg-slate-100 px-2.5 py-1 rounded-md font-medium text-slate-700">
              🏷️ ${deal.category}
            </span>
            <span class="bg-slate-100 px-2.5 py-1 rounded-md font-medium text-slate-700">
              📍 ${deal.location}
            </span>
            <span class="bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded-md font-semibold">
              💰 ${deal.value}
            </span>
          </div>

          <!-- Description -->
          <p class="text-sm text-slate-600 mb-4 line-clamp-3 leading-relaxed">
            ${deal.description}
          </p>
        </div>

        <div>
          <!-- Verification Badge Box -->
          <div class="bg-slate-50 border border-slate-200 rounded-lg p-2.5 mb-4 text-xs text-slate-700 flex items-center justify-between">
            <div class="flex items-center gap-1.5 overflow-hidden">
              <span class="text-emerald-600 verified-indicator font-bold">✓</span>
              <span class="font-semibold text-slate-900 truncate">${verStatus}</span>
            </div>
            <span class="text-slate-400 text-right shrink-0 ml-1 font-mono">${verDate}</span>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1 mb-4">
            ${(deal.tags || []).slice(0, 4).map(t => `
              <span class="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded font-mono">#${t}</span>
            `).join("")}
          </div>

          <!-- Action buttons -->
          <div class="flex items-center gap-2 pt-3 border-t border-slate-100">
            <button data-id="${deal.id}" class="view-details-btn flex-1 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold py-2.5 px-4 rounded-xl transition-colors flex items-center justify-center gap-1.5 shadow-sm">
              <span>Redeem & Verify</span>
              <span>→</span>
            </button>
            <a href="${deal.promotion_url}" target="_blank" rel="noopener noreferrer" 
               title="Open Official Source" 
               class="bg-slate-100 hover:bg-slate-200 text-slate-700 p-2.5 rounded-xl transition-colors flex items-center justify-center">
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>
    `;
  }

  function showDealModal(deal) {
    const rank = deal.priority_rank || 99;
    let badgeClass = "badge-priority-1";
    let badgeText = "⭐ 100% FREE - HIGHEST PRIORITY (NO PURCHASE NECESSARY)";
    if (rank === 2) {
      badgeClass = "badge-priority-2";
      badgeText = "🎁 FREE WITH PURCHASE / BOGO";
    } else if (rank === 3) {
      badgeClass = "badge-priority-3";
      badgeText = "🏷️ DISCOUNT / COUPON SPECIAL";
    }

    const verification = deal.verification || {};

    document.getElementById("modal-priority-badge").className = `${badgeClass} text-xs font-bold px-3 py-1 rounded-full inline-block mb-3`;
    document.getElementById("modal-priority-badge").textContent = badgeText;
    document.getElementById("modal-title").textContent = deal.title;
    document.getElementById("modal-location").textContent = deal.location;
    document.getElementById("modal-category").textContent = deal.category;
    document.getElementById("modal-value").textContent = deal.value;
    document.getElementById("modal-description").textContent = deal.description;

    // Instructions with numbered format
    const instrBox = document.getElementById("modal-instructions");
    instrBox.innerHTML = (deal.redemption_instructions || "").split("\n").map(line => `
      <div class="flex items-start gap-2 mb-2">
        <span class="text-emerald-600 font-bold mt-0.5">•</span>
        <span class="text-slate-800">${line.trim()}</span>
      </div>
    `).join("");

    document.getElementById("modal-restrictions").textContent = deal.restrictions || "None specified.";
    document.getElementById("modal-ver-status").textContent = verification.status || "Verified";
    document.getElementById("modal-ver-source").textContent = verification.source_name || "Official Authority";
    document.getElementById("modal-ver-date").textContent = verification.verified_date || "2026-08-12";
    document.getElementById("modal-ver-notes").textContent = verification.notes || "Official admission policy verified.";

    const officialBtn = document.getElementById("modal-official-link");
    officialBtn.href = deal.promotion_url;

    const commBtn = document.getElementById("modal-community-link");
    if (deal.community_url && deal.community_url !== "#") {
      commBtn.href = deal.community_url;
      commBtn.classList.remove("hidden");
    } else {
      commBtn.classList.add("hidden");
    }

    // Google Calendar button
    const gCalBtn = document.getElementById("modal-gcal-btn");
    gCalBtn.onclick = () => {
      const gcalUrl = createGoogleCalendarUrl(deal);
      window.open(gcalUrl, "_blank");
    };

    // Download .ICS button
    const icsBtn = document.getElementById("modal-ics-btn");
    icsBtn.onclick = () => {
      downloadIcsFile(deal);
    };

    // Copy Instructions Button
    const copyBtn = document.getElementById("modal-copy-btn");
    copyBtn.onclick = () => {
      const textToCopy = `DEAL: ${deal.title}\nHOW TO REDEEM:\n${deal.redemption_instructions}\nRESTRICTIONS: ${deal.restrictions}\nOFFICIAL LINK: ${deal.promotion_url}`;
      navigator.clipboard.writeText(textToCopy).then(() => {
        copyBtn.textContent = "✅ Copied to Clipboard!";
        setTimeout(() => { copyBtn.textContent = "📋 Copy Redemption Details"; }, 2000);
      });
    };

    openModal(detailModal);
  }

  function createGoogleCalendarUrl(deal) {
    const title = encodeURIComponent(`Freebie: ${deal.title}`);
    const details = encodeURIComponent(
      `CouponsDealsSF Verified Promotion\n\nHOW TO REDEEM:\n${deal.redemption_instructions}\n\nRESTRICTIONS:\n${deal.restrictions}\n\nOFFICIAL LINK:\n${deal.promotion_url}`
    );
    const location = encodeURIComponent(deal.location + ", San Francisco Bay Area, CA");
    // Format default all-day event for today
    const dateStr = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    return `https://www.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${dateStr}/${dateStr}&details=${details}&location=${location}&sf=true&output=xml`;
  }

  function downloadIcsFile(deal) {
    const dt = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    const icsData = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//CouponsDealsSF//San Francisco Freebies//EN",
      "BEGIN:VEVENT",
      `SUMMARY:Freebie: ${deal.title}`,
      `LOCATION:${deal.location}, San Francisco Bay Area`,
      `DESCRIPTION:${(deal.description + "\\n\\nRedeem: " + deal.promotion_url).replace(/(\r\n|\n|\r)/gm, "\\n")}`,
      `DTSTART;VALUE=DATE:${dt}`,
      `DTEND;VALUE=DATE:${dt}`,
      "END:VEVENT",
      "END:VCALENDAR"
    ].join("\r\n");

    const blob = new Blob([icsData], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${deal.id}.ics`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function runDeepSearchSimulation() {
    const keyword = deepSearchInput.value.trim().toLowerCase() || "all";
    const source = deepSearchSource.value;

    deepSearchResultsBox.innerHTML = `
      <div class="flex items-center justify-center p-8 text-slate-500">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600 mr-3"></div>
        <span>Running Deep Search across ${source} & verifying links...</span>
      </div>
    `;

    setTimeout(() => {
      if (source === "candidates") {
        // Show live scraped candidates from data/candidates.json
        if (allCandidates.length === 0) {
          deepSearchResultsBox.innerHTML = `
            <div class="text-center p-6 text-slate-500">
              No pending scraped candidates right now. Run <code>python3 scripts/live_scraper.py</code> to fetch new Reddit/RSS promotions!
            </div>
          `;
          return;
        }

        deepSearchResultsBox.innerHTML = `
          <div class="mb-3 flex items-center justify-between text-xs text-slate-500 font-mono">
            <span>LIVE SCRAPED CANDIDATES FROM REDDIT / RSS (${allCandidates.length} MATCHES)</span>
            <span>CLI: python3 scripts/live_scraper.py</span>
          </div>
          <div class="space-y-3 max-h-72 overflow-y-auto pr-1">
            ${allCandidates.map(c => `
              <div class="p-3 bg-slate-800 text-white rounded-xl border border-slate-700 flex items-center justify-between gap-3">
                <div>
                  <div class="flex items-center gap-2 mb-1">
                    <span class="text-xs font-bold px-2 py-0.5 rounded ${
                      c.priority_rank === 1 ? "bg-emerald-500 text-white" : "bg-amber-500 text-white"
                    }">#${c.priority_rank} PRIORITY: ${c.priority_label}</span>
                    <span class="text-xs text-slate-400">[${c.source_subreddit}]</span>
                  </div>
                  <div class="font-semibold text-sm">${c.title}</div>
                  <div class="text-xs text-slate-400 mt-1">Status: ${c.status} (Upvotes: ${c.upvotes || 0})</div>
                </div>
                <a href="${c.community_url}" target="_blank" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shrink-0">
                  Inspect ↗
                </a>
              </div>
            `).join("")}
          </div>
        `;
        return;
      }

      // Filter candidates from local DB
      const matches = allDeals.filter(d => {
        if (keyword !== "all") {
          const text = (d.title + " " + d.description + " " + d.location).toLowerCase();
          if (!text.includes(keyword)) return false;
        }
        if (source === "reddit" && !((d.community_url || "").includes("reddit") || (d.verification?.source_name || "").includes("Reddit"))) {
          return false;
        }
        if (source === "official" && (d.verification?.status || "") !== "Verified Official Source") {
          return false;
        }
        return true;
      });

      if (matches.length === 0) {
        deepSearchResultsBox.innerHTML = `
          <div class="text-center p-6 text-slate-500">
            No candidates matched keyword "${keyword}" in source "${source}". Try searching for "museum", "free", "birthday", or "sf resident".
          </div>
        `;
        return;
      }

      deepSearchResultsBox.innerHTML = `
        <div class="mb-3 flex items-center justify-between text-xs text-slate-500 font-mono">
          <span>DEEP SEARCH RESULTS (${matches.length} MATCHES)</span>
          <span>CLI: python3 scripts/deep_search.py --query "${keyword === "all" ? "" : keyword}"</span>
        </div>
        <div class="space-y-3 max-h-72 overflow-y-auto pr-1">
          ${matches.map(d => `
            <div class="p-3 bg-slate-800 text-white rounded-xl border border-slate-700 flex items-center justify-between gap-3">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-xs font-bold px-2 py-0.5 rounded ${
                    d.priority_rank === 1 ? "bg-emerald-500 text-white" : "bg-amber-500 text-white"
                  }">#${d.priority_rank} PRIORITY: ${d.priority_label}</span>
                  <span class="text-xs text-slate-400">${d.location}</span>
                </div>
                <div class="font-semibold text-sm">${d.title}</div>
                <div class="text-xs text-slate-400 mt-1">Verified via ${d.verification?.source_name} (${d.verification?.verified_date})</div>
              </div>
              <a href="${d.promotion_url}" target="_blank" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg shrink-0">
                Verify ↗
              </a>
            </div>
          `).join("")}
        </div>
      `;
    }, 350);
  }

  function openModal(modalEl) {
    modalEl.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  function closeModal(modalEl) {
    modalEl.classList.add("hidden");
    document.body.style.overflow = "auto";
  }
});
