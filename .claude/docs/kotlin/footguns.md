# Kotlin Footguns

Version: Kotlin 1.9+ / kotlinx.coroutines 1.7+

## 1. StateFlow Conflation Drops Intermediate States

`MutableStateFlow` conflates emissions — if you emit A, B, C rapidly, collectors may only see A and C. This is by design (latest-state semantics), but it means you cannot use StateFlow for event streams where every emission matters.

**Fix**: Use `SharedFlow` with `extraBufferCapacity` for events. Use `StateFlow` only for state holders.

## 2. data class copy() Shares Mutable References

```kotlin
data class GameState(val players: MutableMap<PlayerId, Player>)

val copy = state.copy() // SAME mutable map instance!
copy.players[id] = newPlayer // mutates the original too
```

**Fix**: Use immutable collections (`Map`, `List`) in data classes. If you must copy mutable state, deep-copy explicitly.

## 3. synchronized Blocks in Coroutine Context

`synchronized(lock) { ... }` blocks the underlying thread. In a coroutine, this prevents other coroutines from running on that thread, defeating the purpose of cooperative scheduling.

```kotlin
// BAD: blocks thread
fun dispatch(intent: GameIntent) = synchronized(lock) { /* ... */ }

// GOOD: suspends cooperatively
private val mutex = Mutex()
suspend fun dispatch(intent: GameIntent) = mutex.withLock { /* ... */ }
```

**Exception**: Acceptable if the critical section is very short (< 1ms) and never calls suspend functions.

## 4. CancellationException Must Not Be Caught Generically

```kotlin
// BAD: swallows cancellation, breaks structured concurrency
try { suspendingWork() } catch (e: Exception) { log(e) }

// GOOD: rethrow CancellationException
try { suspendingWork() } catch (e: CancellationException) { throw e } catch (e: Exception) { log(e) }

// BETTER: use runCatching only for non-suspending code
// For suspending code, catch specific exception types
```

## 5. Flow Collection in init{} Without Lifecycle Awareness

```kotlin
// BAD: collects forever, even when ViewModel is cleared
init {
    viewModelScope.launch {
        someFlow.collect { /* ... */ } // never stops until scope cancelled
    }
}
```

This is actually fine in ViewModels (viewModelScope cancels on clear), but in Activities/Fragments, use `repeatOnLifecycle(Lifecycle.State.STARTED)`.

## 6. MutableStateFlow.update{} vs .value = (Race Conditions)

```kotlin
// BAD: race condition if called from multiple coroutines
_state.value = _state.value.copy(count = _state.value.count + 1)

// GOOD: atomic read-modify-write
_state.update { it.copy(count = it.count + 1) }
```

`update{}` uses CAS (compare-and-swap) internally. Always prefer it over direct `.value` assignment when the new value depends on the old value.

## 7. UUID.randomUUID() Security

`UUID.randomUUID()` uses `SecureRandom` on most JVM implementations (OpenJDK, Android), but this is **not guaranteed by the spec**. For security-critical tokens (auth tokens, session secrets), use `SecureRandom` directly.

```kotlin
// For auth tokens — use SecureRandom explicitly
val bytes = ByteArray(32)
SecureRandom().nextBytes(bytes)
val token = bytes.joinToString("") { "%02x".format(it) }

// For non-security IDs (rollId, sessionId) — UUID is fine
val id = UUID.randomUUID().toString()
```

## 8. kotlinx.serialization Polymorphic Registration

Polymorphic serialization requires explicit module registration. Without it, you get runtime `SerializationException`.

```kotlin
// REQUIRED for sealed class hierarchies sent over the wire
val json = Json {
    serializersModule = SerializersModule {
        polymorphic(GameMessage::class) {
            subclass(RollResultMsg::class, RollResultMsg.serializer())
            subclass(PlayerJoinedMsg::class, PlayerJoinedMsg.serializer())
            // every subclass must be registered
        }
    }
}
```

Sealed classes with `@Serializable` on the base AND all subclasses auto-register in Kotlin 1.9+, but only if the `classDiscriminator` matches (default: `"type"`).

## 9. Kotlin == vs === Confusion

- `==` calls `equals()` (structural equality)
- `===` checks reference identity

Data classes generate `equals()` from all constructor properties. Two data class instances with the same values are `==` but not `===`. This is usually correct, but be careful with mutable properties in equals.

## 10. Sealed when Exhaustiveness: Expression vs Statement

```kotlin
// EXPRESSION: compiler enforces exhaustiveness
val result = when (msg) {
    is RollResult -> handle(msg)
    is PlayerJoined -> handle(msg)
    // compile error if branch missing
}

// STATEMENT: compiler does NOT enforce exhaustiveness
when (msg) {
    is RollResult -> handle(msg)
    // missing branches: no compile error!
}
```

**Fix**: Use `when` as an expression (assign to val or return) whenever matching sealed types. Or add an `else -> error("Unhandled: $msg")` to catch missing branches at runtime.
