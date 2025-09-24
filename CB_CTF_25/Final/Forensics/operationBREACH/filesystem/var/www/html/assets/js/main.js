/**
 * GridSecure Industries Main JavaScript
 * Version: 2.1.4
 * Last Updated: 2023-10-10
 */

// Global configuration
const APP_CONFIG = {
  apiEndpoint: "/api/v1",
  sessionTimeout: 3600,
  debugMode: false,
  version: "2.1.4",
};

// Utility functions
const Utils = {
  // Format currency
  formatCurrency: function (amount, currency = "USD") {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: currency,
    }).format(amount);
  },

  // Format date
  formatDate: function (date) {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(date));
  },

  // Show notification
  showNotification: function (message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `alert alert-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  },

  // Validate email
  validateEmail: function (email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  // Debounce function
  debounce: function (func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },
};

// Session management
const SessionManager = {
  checkSession: function () {
    const lastActivity = localStorage.getItem("lastActivity");
    const now = Date.now();

    if (
      lastActivity &&
      now - parseInt(lastActivity) > APP_CONFIG.sessionTimeout * 1000
    ) {
      this.logout();
      return false;
    }

    localStorage.setItem("lastActivity", now.toString());
    return true;
  },

  logout: function () {
    localStorage.removeItem("lastActivity");
    window.location.href = "/login.php";
  },

  init: function () {
    // Check session every minute
    setInterval(() => {
      this.checkSession();
    }, 60000);

    // Update last activity on user interaction
    document.addEventListener("click", () => {
      localStorage.setItem("lastActivity", Date.now().toString());
    });
  },
};

// Form validation
const FormValidator = {
  validateForm: function (form) {
    const inputs = form.querySelectorAll(
      "input[required], select[required], textarea[required]"
    );
    let isValid = true;

    inputs.forEach((input) => {
      if (!input.value.trim()) {
        this.showError(input, "This field is required");
        isValid = false;
      } else {
        this.clearError(input);
      }
    });

    return isValid;
  },

  showError: function (input, message) {
    const errorDiv =
      input.parentNode.querySelector(".error-message") ||
      document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.textContent = message;
    errorDiv.style.color = "#dc3545";
    errorDiv.style.fontSize = "0.875rem";
    errorDiv.style.marginTop = "0.25rem";

    if (!input.parentNode.querySelector(".error-message")) {
      input.parentNode.appendChild(errorDiv);
    }

    input.style.borderColor = "#dc3545";
  },

  clearError: function (input) {
    const errorDiv = input.parentNode.querySelector(".error-message");
    if (errorDiv) {
      errorDiv.remove();
    }
    input.style.borderColor = "#ddd";
  },
};

// API client
const ApiClient = {
  request: async function (endpoint, options = {}) {
    const url = APP_CONFIG.apiEndpoint + endpoint;
    const config = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      Utils.showNotification(
        "An error occurred while processing your request",
        "error"
      );
      throw error;
    }
  },

  get: function (endpoint) {
    return this.request(endpoint);
  },

  post: function (endpoint, data) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};

// Initialize application
document.addEventListener("DOMContentLoaded", function () {
  // Initialize session manager
  SessionManager.init();

  // Add form validation
  const forms = document.querySelectorAll("form[data-validate]");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      if (!FormValidator.validateForm(this)) {
        e.preventDefault();
      }
    });
  });

  // Add loading states to buttons
  const buttons = document.querySelectorAll('button[type="submit"]');
  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      if (this.form && FormValidator.validateForm(this.form)) {
        this.disabled = true;
        this.textContent = "Processing...";
      }
    });
  });

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  if (APP_CONFIG.debugMode) {
    console.log("GridSecure Industries initialized");
    console.log("Version:", APP_CONFIG.version);
  }
});

// Export for module systems
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    Utils,
    SessionManager,
    FormValidator,
    ApiClient,
    APP_CONFIG,
  };
}
