/**
 * @param {string} url - The URL to fetch from
 * @returns {Promise<Object>} - The fetched data
 * @throws {Error} - If the request fails
 */
async function mockApiCall(url) {
  // Simulate network delay (0-500ms)
  const delay = Math.random() * 500;
  await new Promise((resolve) => setTimeout(resolve, delay));

  // Randomly succeed (70% chance) or fail (30% chance)
  if (Math.random() < 0.7) {
    return {
      success: true,
      data: {
        url: url,
        timestamp: new Date().toISOString(),
        message: "Data fetched successfully",
      },
    };
  } else {
    throw new Error(`Failed to fetch data from ${url}`);
  }
}

/**
 * Fetches data from a URL with automatic retry logic.
 *
 * @param {string} url - The URL to fetch data from
 * @param {number} maxRetries - Maximum number of retry attempts (default: 3)
 * @param {number} retryDelay - Delay between retries in milliseconds (default: 1000)
 * @returns {Promise<Object>} - The fetched data
 * @throws {Error} - If all retry attempts fail
 */
async function fetchWithRetry(url, maxRetries = 3, retryDelay = 1000) {
  // Validate inputs
  if (!url || typeof url !== "string") {
    throw new Error("URL must be a non-empty string");
  }

  if (maxRetries < 0 || !Number.isInteger(maxRetries)) {
    throw new Error("maxRetries must be a non-negative integer");
  }

  if (retryDelay < 0 || typeof retryDelay !== "number") {
    throw new Error("retryDelay must be a non-negative number");
  }

  let lastError;

  // Attempt fetch with retries
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const data = await mockApiCall(url);
      console.log(`✓ Success on attempt ${attempt + 1}/${maxRetries + 1}`);
      return data;
    } catch (error) {
      lastError = error;

      // Don't wait after the last attempt
      if (attempt < maxRetries) {
        console.log(
          `Attempt ${attempt + 1}/${maxRetries + 1} failed: ${error.message}`
        );
        console.log(`  Retrying in ${retryDelay}ms...`);
        await new Promise((resolve) => setTimeout(resolve, retryDelay));
      } else {
        console.log(
          `Final attempt ${attempt + 1}/${maxRetries + 1} failed: ${
            error.message
          }`
        );
      }
    }
  }

  // All retries exhausted
  throw new Error(
    `Failed to fetch data from ${url} after ${
      maxRetries + 1
    } attempts. Last error: ${lastError.message}`
  );
}

/**
 * Helper function to create a delay (sleep).
 *
 * @param {number} ms - Milliseconds to wait
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Example usage and testing
async function main() {
  console.log("=".repeat(60));
  console.log("Async Data Fetcher with Retry - Example");
  console.log("=".repeat(60));

  const testUrl = "https://api.example.com/data";

  // Test 1: Successful fetch (may take a few attempts)
  console.log("\nTest 1: Fetching with retry (max 3 retries)");
  console.log("-".repeat(60));
  try {
    const result = await fetchWithRetry(testUrl, 3);
    console.log("\n Final Result:", JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("\n Final Error:", error.message);
  }

  // Test 2: With custom retry count
  console.log("\n\nTest 2: Fetching with 5 retries");
  console.log("-".repeat(60));
  try {
    const result = await fetchWithRetry(testUrl, 5);
    console.log("\n Final Result:", JSON.stringify(result, null, 2));
  } catch (error) {
    console.error("\n Final Error:", error.message);
  }
}

// Export for use in other modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    fetchWithRetry,
    mockApiCall,
    sleep,
  };
}

// Run example if executed directly
if (typeof require !== "undefined" && require.main === module) {
  main().catch(console.error);
}
