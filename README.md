# EA Project - Three Programming Tasks

This repository contains implementations of three programming tasks:

1. **Smart Text Analyzer** (Python)
2. **Async Data Fetcher with Retry** (JavaScript)
3. **Rate Limiter** (Python)

---

## 📋 Table of Contents

- [Task 1: Smart Text Analyzer](#task-1-smart-text-analyzer)
- [Task 2: Async Data Fetcher with Retry](#task-2-async-data-fetcher-with-retry)
- [Task 3: Rate Limiter](#task-3-rate-limiter)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

---

## Task 1: Smart Text Analyzer

### Description

A Python function that analyzes text and returns comprehensive statistics including word count, average word length, longest words, and word frequency.

### Features

- ✅ Total word count
- ✅ Average word length (2 decimal places)
- ✅ Longest word(s) - returns all if tied
- ✅ Word frequency (case-insensitive)
- ✅ Handles punctuation correctly
- ✅ Edge case handling (empty strings, whitespace)

### Usage

```python
from task1_text_analyzer import analyze_text

text = "The quick brown fox jumps over the lazy dog the fox"
result = analyze_text(text)

print(result)
# {
#     "word_count": 10,
#     "average_word_length": 3.70,
#     "longest_words": ["quick", "brown", "jumps"],
#     "word_frequency": {"the": 2, "quick": 1, "fox": 2, ...}
# }
```

### Run Example

```bash
python task1_text_analyzer.py
```

### Run Tests

```bash
python test_task1.py
```

---

## Task 2: Async Data Fetcher with Retry

### Description

A JavaScript function that fetches data from a URL with automatic retry logic. Uses async/await and includes a mock API function for testing.

### Features

- ✅ Fetches data from URL (with mock implementation)
- ✅ Automatic retry on failure
- ✅ Configurable retry count and delay
- ✅ Waits 1 second between retries (configurable)
- ✅ Comprehensive error handling
- ✅ Input validation
- ✅ Works in Node.js and browsers

### Usage

#### Node.js

```javascript
const { fetchWithRetry } = require("./task2_async_fetcher");

async function example() {
  try {
    const data = await fetchWithRetry("https://api.example.com/data", 3);
    console.log(data);
  } catch (error) {
    console.error("All retries failed:", error.message);
  }
}
```

#### Browser/ES6 Modules

```javascript
import { fetchWithRetry } from "./task2_async_fetcher.js";

// Same usage as above
```

### Parameters

- `url` (string): The URL to fetch from
- `maxRetries` (number, default: 3): Maximum number of retry attempts
- `retryDelay` (number, default: 1000): Delay between retries in milliseconds

### Run Example

```bash
node task2_async_fetcher.js
```

### Run Tests

```bash
node test_task2.js
```

### Production Usage

Replace `mockApiCall` with actual fetch:

```javascript
// In fetchWithRetry function, replace:
const data = await mockApiCall(url);

// With:
const response = await fetch(url);
if (!response.ok) {
  throw new Error(`HTTP ${response.status}: ${response.statusText}`);
}
return await response.json();
```

---

## Task 3: Rate Limiter

### Description

A Python rate limiter that limits requests per user within a time window. Thread-safe and includes automatic cleanup of expired entries.

### Features

- ✅ Limits: 5 requests per 60 seconds per user (configurable)
- ✅ Per-user tracking
- ✅ Blocks requests when limit exceeded
- ✅ Auto-resets after time window
- ✅ Thread-safe for concurrent requests
- ✅ Automatic cleanup of expired entries
- ✅ Status checking without making request
- ✅ Manual reset capabilities

### Usage

```python
from task3_rate_limiter import RateLimiter

# Create rate limiter: 5 requests per 60 seconds
limiter = RateLimiter(max_requests=5, window_seconds=60)

# Check if request is allowed
user_id = "user123"
allowed, info = limiter.is_allowed(user_id)

if allowed:
    print(f"Request allowed. Remaining: {info['remaining_requests']}")
    # Process request...
else:
    print(f"Rate limited. Try again in {info['time_until_reset']:.1f} seconds")
```

### Methods

#### `is_allowed(user_id, current_time=None)`

Check if a request is allowed for a user.

- Returns: `(bool, dict)` - (is_allowed, status_info)

#### `get_status(user_id, current_time=None)`

Get current rate limit status without making a request.

- Returns: `dict` - Status information

#### `reset_user(user_id)`

Reset rate limit for a specific user.

#### `reset_all()`

Reset rate limit for all users.

### Custom Limits

```python
# Custom: 10 requests per 30 seconds
limiter = RateLimiter(max_requests=10, window_seconds=30)
```

### Run Example

```bash
python task3_rate_limiter.py
```

### Run Tests

```bash
python test_task3.py
```

### Example Output

```
Request 1: ✓ ALLOWED
  Current requests: 1/5
  Remaining: 4

Request 2: ✓ ALLOWED
  Current requests: 2/5
  Remaining: 3

...

Request 6: ✗ BLOCKED
  Current requests: 5/5
  Time until reset: 45.3s
```

---

## Running Tests

### All Tests

```bash
# Python tests
python test_task1.py
python test_task3.py

# JavaScript tests
node test_task2.js
```

### Expected Test Results

- **Task 1**: All tests should pass (8 test cases)
- **Task 2**: Tests should pass (4 test cases)
- **Task 3**: All tests should pass (9 test cases)

---

## Project Structure

```
eaglepoint-project/
│
├── task1_text_analyzer.py      # Smart Text Analyzer implementation
├── test_task1.py                # Tests for Task 1
│
├── task2_async_fetcher.js       # Async Data Fetcher with Retry
├── test_task2.js                # Tests for Task 2
│
├── task3_rate_limiter.py        # Rate Limiter implementation
├── test_task3.py                # Tests for Task 3
│
├── README.md                    # This file
└── DOCUMENTATION.md             # Complete documentation of process
```

---

## Requirements

### Python

- Python 3.6+ (for type hints and f-strings)
- Standard library only (no external dependencies)

### JavaScript

- Node.js 12+ (for async/await support)
- Or modern browser with ES6+ support

---

## Code Quality

All code follows best practices:

- ✅ Clean, readable code with meaningful names
- ✅ Comprehensive error handling
- ✅ Comments for complex logic
- ✅ Type hints (Python) and JSDoc (JavaScript)
- ✅ Edge case handling
- ✅ Input validation
- ✅ Test coverage

---

## Why These Solutions?

### Task 1: Python

- Excellent text processing libraries
- `Counter` for efficient frequency counting
- Regex for accurate word extraction
- Clean, readable syntax

### Task 2: JavaScript

- Required by task specification
- Native async/await support
- Works in both Node.js and browsers
- Modern Promise API

### Task 3: Python

- `deque` for efficient FIFO operations
- `threading.Lock` for thread safety
- `defaultdict` simplifies per-user tracking
- Excellent for data structure problems

---
