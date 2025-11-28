# Complete Documentation - Eaglepoint Project Tasks

## Table of Contents

1. [Task 1: Smart Text Analyzer](#task-1-smart-text-analyzer)
2. [Task 2: Async Data Fetcher with Retry](#task-2-async-data-fetcher-with-retry)
3. [Task 3: Rate Limiter](#task-3-rate-limiter)

---

## Task 1: Smart Text Analyzer

### Research and Searches

**Search 1: Python text analysis best practices**

- **Query**: "python count words in string best practice"
- **URL**: https://stackoverflow.com/questions/19410018/how-to-count-the-number-of-words-in-a-sentence-ignoring-spaces-punctuation
- **Result**: Learned about using `re.findall()` with word boundary regex patterns for accurate word extraction

**Search 2: Python word frequency counting**

- **Query**: "python count word frequency case insensitive collections Counter"
- **URL**: https://docs.python.org/3/library/collections.html#collections.Counter
- **Result**: Confirmed that `Counter` from `collections` is the optimal way to count frequencies

**Search 3: Python regex word boundaries**

- **Query**: "python regex \b word boundary punctuation"
- **URL**: https://docs.python.org/3/library/re.html
- **Result**: Understood that `\b\w+\b` pattern correctly handles word boundaries and excludes punctuation

### Thought Process

**Why Python?**

- Python excels at text processing with built-in libraries
- `collections.Counter` provides efficient frequency counting
- `re` module offers powerful regex capabilities
- Clean, readable syntax for this type of task

**Alternatives Considered:**

1. **JavaScript**: Good for web integration, but Python's text processing libraries are more mature
2. **Go**: Fast but more verbose for text manipulation
3. **Java**: Verbose syntax, overkill for this task

**Approach Decision:**

- Use `re.findall(r'\b\w+\b', text.lower())` for word extraction
  - Handles punctuation correctly
  - Case-insensitive via `.lower()`
  - Word boundaries ensure accurate counting
- Use `Counter` for frequency counting (O(n) time complexity)
- Calculate average by summing lengths and dividing
- Find longest words by filtering words with max length

### Step-by-Step Solution Process

**Step 1: Word Extraction**

- Problem: Need to handle punctuation, whitespace, and case-insensitivity
- Solution: Used regex `\b\w+\b` pattern which:
  - `\b` = word boundary (handles punctuation)
  - `\w+` = one or more word characters
  - Applied `.lower()` for case-insensitive processing

**Step 2: Word Count**

- Simple: `len(words)` after extraction
- Handled edge case: empty strings return 0

**Step 3: Average Word Length**

- Formula: `sum(len(word) for word in words) / len(words)`
- Used `round(..., 2)` for 2 decimal places as required
- Edge case: Division by zero handled with early return

**Step 4: Longest Words**

- Problem: Need all words if there's a tie
- Solution:
  1. Find max length: `max(len(word) for word in words)`
  2. Filter words with that length
  3. Remove duplicates with `set()`
  4. Sort for consistent output

**Step 5: Word Frequency**

- Used `Counter(words)` which automatically counts frequencies
- Converted to dict for JSON serialization
- Already case-insensitive due to `.lower()` preprocessing

**Problems Faced:**

1. **Punctuation handling**: Initially tried `split()` which doesn't handle punctuation well
   - **Fix**: Switched to regex with word boundaries
2. **Tied longest words**: Initially only returned first longest word
   - **Fix**: Filter all words with max length, use set to remove duplicates
3. **Empty input**: Division by zero error
   - **Fix**: Early return with default values

### Why This Solution is Best

1. **Accuracy**: Regex word boundaries correctly handle punctuation (e.g., "Hello, world!" → ["hello", "world"])
2. **Efficiency**:
   - Single pass through text for word extraction: O(n)
   - Counter for frequency: O(n)
   - Overall: O(n) time complexity
3. **Robustness**: Handles edge cases (empty strings, whitespace-only, punctuation)
4. **Maintainability**: Clean, readable code with type hints and docstrings
5. **Correctness**: Matches expected output format exactly

---

## Task 2: Async Data Fetcher with Retry

### Research and Searches

**Search 1: JavaScript async/await retry pattern**

- **Query**: "javascript async await retry pattern best practices"
- **URL**: https://stackoverflow.com/questions/38213668/retry-logic-for-async-await
- **Result**: Learned about using for loops with try-catch for retry logic

**Search 2: JavaScript fetch API error handling**

- **Query**: "javascript fetch api error handling retry"
- **URL**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- **Result**: Understood proper error handling for fetch API

**Search 3: JavaScript Promise delay/sleep**

- **Query**: "javascript promise delay sleep setTimeout"
- **URL**: https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
- **Result**: Confirmed `new Promise(resolve => setTimeout(resolve, ms))` pattern

### Thought Process

**Why JavaScript?**

- Task explicitly requires JavaScript
- Native async/await support
- Modern Promise API for delays
- Can be used in both Node.js and browsers

**Alternatives Considered:**

1. **Promise chains**: More verbose than async/await
2. **Recursive retry**: Could cause stack overflow with many retries
3. **Library (axios-retry)**: Overkill, want to show understanding of core concepts

**Approach Decision:**

- Use `async/await` for clean, readable code
- For loop with try-catch for retry logic (avoids recursion issues)
- `setTimeout` wrapped in Promise for delays
- Separate mock function for testing (can be replaced with real fetch)

### Step-by-Step Solution Process

**Step 1: Mock API Function**

- Problem: Need to simulate API calls that randomly succeed/fail
- Solution: Created `mockApiCall()` that:
  - Simulates network delay (0-500ms)
  - Randomly succeeds (70%) or fails (30%)
  - Returns proper data structure on success
  - Throws error on failure

**Step 2: Retry Logic**

- Problem: Need to retry on failure, wait between retries, stop after max attempts
- Solution:
  - For loop: `for (let attempt = 0; attempt <= maxRetries; attempt++)`
  - Try-catch inside loop
  - On success: return immediately
  - On failure: wait (if not last attempt), then continue

**Step 3: Delay Between Retries**

- Problem: Need to wait 1 second between retries
- Solution: `await new Promise(resolve => setTimeout(resolve, retryDelay))`
- Only wait if not the last attempt

**Step 4: Error Handling**

- Problem: Need to throw meaningful error after all retries fail
- Solution: Store last error, throw comprehensive error message with attempt count

**Step 5: Input Validation**

- Problem: Should validate inputs for robustness
- Solution: Added checks for:
  - URL must be non-empty string
  - maxRetries must be non-negative integer
  - retryDelay must be non-negative number

**Problems Faced:**

1. **Waiting after last attempt**: Initially waited even after final failure
   - **Fix**: Only wait if `attempt < maxRetries`
2. **Error message clarity**: Initial errors weren't descriptive
   - **Fix**: Added attempt numbers and comprehensive error messages
3. **Module exports**: Needed to work in both Node.js and browser
   - **Fix**: Conditional export using `module.exports` check

### Why This Solution is Best

1. **Clean Code**: async/await is more readable than Promise chains
2. **Robust**: Input validation prevents runtime errors
3. **Flexible**: Configurable retry count and delay
4. **Informative**: Logs each attempt for debugging
5. **Production-Ready**: Easy to replace mock with real fetch API
6. **Error Handling**: Comprehensive error messages help debugging
7. **No Stack Overflow**: Iterative approach (not recursive)

---

## Task 3: Rate Limiter

### Research and Searches

**Search 1: Rate limiting algorithms sliding window**

- **Query**: "rate limiting algorithm sliding window python implementation"
- **URL**: https://en.wikipedia.org/wiki/Rate_limiting
- **Result**: Learned about sliding window vs fixed window approaches

**Search 2: Python deque for time-based data**

- **Query**: "python deque time-based data structure efficient"
- **URL**: https://docs.python.org/3/library/collections.html#collections.deque
- **Result**: Confirmed deque is efficient for FIFO operations (O(1) append/popleft)

**Search 3: Thread-safe rate limiting Python**

- **Query**: "python thread safe rate limiter threading Lock"
- **URL**: https://docs.python.org/3/library/threading.html#threading.Lock
- **Result**: Understood need for Lock when multiple threads access shared state

**Search 4: Rate limiting best practices**

- **Query**: "rate limiter design pattern per user tracking"
- **URL**: https://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm
- **Result**: Learned about per-user tracking and automatic cleanup

### Thought Process

**Why Python?**

- Excellent for this type of data structure problem
- `deque` provides efficient FIFO operations
- `threading.Lock` for thread safety
- `defaultdict` simplifies per-user tracking

**Alternatives Considered:**

1. **Fixed Window**: Simpler but less accurate (bursts at window boundaries)
2. **Token Bucket**: More complex, overkill for this requirement
3. **Sliding Window with Redis**: Better for distributed systems, but adds dependency
4. **Sliding Window (deque)**: Best balance of accuracy and simplicity

**Approach Decision:**

- Sliding window using `deque` to store timestamps
- Per-user tracking with dictionary: `{user_id: deque([timestamps])}`
- Automatic cleanup of expired entries on each check
- Thread-safe using `Lock` for concurrent access

### Step-by-Step Solution Process

**Step 1: Data Structure Design**

- Problem: Need to track requests per user within time window
- Solution:
  - `defaultdict(deque)` for per-user timestamp storage
  - `deque` allows efficient O(1) append and popleft operations
  - Each user has their own deque of timestamps

**Step 2: Request Check Logic**

- Problem: Need to check if request is allowed, clean expired entries, add new request
- Solution:
  1. Get user's deque (create if doesn't exist)
  2. Remove expired timestamps (older than `current_time - window_seconds`)
  3. Check if count < max_requests
  4. If allowed: append current timestamp
  5. Return status with detailed info

**Step 3: Automatic Cleanup**

- Problem: Need to remove old timestamps to prevent memory growth
- Solution: On each `is_allowed()` call, remove timestamps older than window
- Uses `popleft()` in while loop until all expired entries removed
- O(k) where k = expired entries (typically small)

**Step 4: Thread Safety**

- Problem: Multiple threads might access rate limiter simultaneously
- Solution: Use `threading.Lock()` to protect critical sections
- All operations on `_requests` dictionary wrapped in `with self._lock:`

**Step 5: Status and Reset Methods**

- Added `get_status()` for checking without making request
- Added `reset_user()` for manual user reset
- Added `reset_all()` for complete reset

**Problems Faced:**

1. **Memory growth**: Initially didn't clean expired entries
   - **Fix**: Added cleanup logic in `is_allowed()` and `get_status()`
2. **Race conditions**: Multiple threads could corrupt state
   - **Fix**: Added `Lock` around all dictionary operations
3. **Time calculation**: Needed to handle time_until_reset correctly
   - **Fix**: Calculate based on oldest request timestamp
4. **Edge case handling**: Empty deque, zero requests, etc.
   - **Fix**: Added proper checks and default values

### Why This Solution is Best

1. **Accurate**: Sliding window provides precise rate limiting (no burst issues)
2. **Efficient**:
   - O(1) append/popleft operations
   - O(k) cleanup where k = expired entries (typically small)
   - Memory efficient: only stores timestamps within window
3. **Thread-Safe**: Lock ensures correct behavior with concurrent requests
4. **Automatic Cleanup**: Prevents memory leaks by removing expired entries
5. **Flexible**: Configurable limits and window size
6. **Informative**: Returns detailed status information
7. **Production-Ready**: Can be easily extended (e.g., Redis backend for distributed systems)

---

## Summary

All three tasks were completed with:

- ✅ Clean, readable code following best practices
- ✅ Comprehensive error handling
- ✅ Detailed comments for complex logic
- ✅ Test suites for verification
- ✅ Production-ready implementations
- ✅ Complete documentation of process

Each solution was chosen after considering alternatives and represents the optimal approach for the specific requirements.
