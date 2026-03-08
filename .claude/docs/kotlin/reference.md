# Kotlin Reference — Key APIs

Version: Kotlin 1.9+ / kotlinx.coroutines 1.7+ / kotlinx.serialization 1.6+

## kotlinx.coroutines

### Builders
- `launch {}` — fire-and-forget coroutine, returns `Job`
- `async {}` — returns `Deferred<T>`, call `.await()` for result
- `runBlocking {}` — bridges blocking/suspending world (tests, main functions only)
- `coroutineScope {}` — creates child scope, suspends until all children complete, propagates failures
- `supervisorScope {}` — like coroutineScope but child failures don't cancel siblings

### Flow
- `flow {}` — cold flow builder, `emit()` inside
- `MutableStateFlow(initial)` — hot state holder, `.value`, `.update {}`, conflates
- `MutableSharedFlow(replay, extraBufferCapacity)` — hot event stream, configurable buffering
- `.map {}`, `.filter {}`, `.flatMapLatest {}` — standard operators
- `.stateIn(scope, started, initialValue)` — convert cold flow to StateFlow
- `.shareIn(scope, started, replay)` — convert cold flow to SharedFlow
- `combine(flow1, flow2) { a, b -> }` — combine latest values from multiple flows
- `.debounce(timeMillis)` — emit only after quiet period
- `.distinctUntilChanged()` — skip consecutive duplicates

### Dispatchers
- `Dispatchers.Main` — Android main thread (Compose, UI updates)
- `Dispatchers.IO` — thread pool for blocking I/O (file, network, database)
- `Dispatchers.Default` — CPU-intensive work (parsing, computation)
- `Dispatchers.Unconfined` — resumes in caller thread (testing only)
- `newSingleThreadContext("name")` — dedicated thread (serialized access)

### Synchronization
- `Mutex()` — cooperative lock for coroutines (`.withLock {}`)
- `Channel<T>()` — CSP-style communication between coroutines
- `Semaphore(permits)` — limit concurrent access

## kotlinx.serialization

### Annotations
- `@Serializable` — generate serializer for class
- `@SerialName("wire_name")` — override JSON key name
- `@Transient` — exclude from serialization (must have default value)
- `@EncodeDefault` — include in output even if matches default

### Json Configuration
```kotlin
val json = Json {
    ignoreUnknownKeys = true      // forward compatibility
    encodeDefaults = false         // skip default values in output
    classDiscriminator = "type"    // polymorphic type field name
    prettyPrint = false            // compact output
}
```

### Polymorphic Serialization
Sealed class hierarchies with `@Serializable` on base + subclasses auto-register.
The `classDiscriminator` field (default `"type"`) is added to JSON output:
```json
{"type": "roll_result", "seq": 1, "entry": {...}}
```

## Kotlin Standard Library

### Collections
- `listOf()`, `mutableListOf()`, `emptyList()`
- `mapOf()`, `mutableMapOf()`, `emptyMap()`
- `setOf()`, `mutableSetOf()`, `emptySet()`
- `.associateBy { key }` — List → Map by key
- `.groupBy { key }` — List → Map<K, List<V>>
- `.partition { predicate }` — List → Pair<List, List>
- `.mapNotNull { transform }` — map + filter nulls
- `.flatMap { transform }` — map + flatten
- `.sortedBy { selector }` — sorted copy
- `.distinctBy { selector }` — unique by selector

### Null Safety
- `?.` safe call — returns null if receiver is null
- `?:` elvis — provides default for null
- `!!` not-null assertion — throws NPE if null (avoid in production code)
- `requireNotNull(value) { "msg" }` — throws IllegalArgumentException
- `checkNotNull(value) { "msg" }` — throws IllegalStateException

### String
- `"Hello, ${name}"` — string templates
- `"""multiline"""` — raw strings (no escaping needed)
- `.trimIndent()` — strip common leading whitespace from multiline

## JUnit 5 with Kotlin

```kotlin
class GameStateReducerTest {
    @Test
    fun `player joins lobby successfully`() {
        val state = lobbyState()
        val (newState, messages) = reducer.reduce(state, JoinPlayer("Alice"))
        assertEquals(1, newState.players.size)
        assertInstanceOf(PlayerJoinedMsg::class.java, messages.first())
    }

    @Nested
    inner class RollTests {
        @Test
        fun `blind roll stays COMPLETED`() { /* ... */ }
    }
}
```

- Backtick test names for readability
- `@Nested inner class` for grouping
- `assertThrows<ExceptionType> { code }` for exception testing

## Turbine (Flow testing)

```kotlin
@Test
fun `state updates on dispatch`() = runTest {
    viewModel.state.test {
        assertEquals(initialState, awaitItem())
        viewModel.doSomething()
        assertEquals(expectedState, awaitItem())
        cancelAndIgnoreRemainingEvents()
    }
}
```
