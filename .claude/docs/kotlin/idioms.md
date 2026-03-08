# Kotlin Idioms

Version: Kotlin 1.9+ / kotlinx.coroutines 1.7+

## 1. Sealed Class Hierarchies for State Machines

```kotlin
sealed class SessionState {
    data object Created : SessionState()
    data object Lobby : SessionState()
    data class Active(val startedAt: Instant) : SessionState()
    data object Ended : SessionState()
}

// Exhaustive when-expression (compiler enforced)
fun render(state: SessionState) = when (state) {
    is SessionState.Created -> "Waiting..."
    is SessionState.Lobby -> "In lobby"
    is SessionState.Active -> "Playing since ${state.startedAt}"
    is SessionState.Ended -> "Game over"
}
```

## 2. Sealed Interfaces for Message Types

```kotlin
sealed interface GameMessage {
    val seq: Long
    data class RollResult(override val seq: Long, val entry: RollEntry) : GameMessage
    data class PlayerJoined(override val seq: Long, val player: Player) : GameMessage
}
```

Prefer sealed interface over sealed class when no shared state — allows implementing multiple sealed hierarchies.

## 3. Extension Functions for Domain DSLs

```kotlin
fun GameState.playerById(id: PlayerId): Player? = players[id]
fun List<RollEntry>.forPlayer(id: PlayerId) = filter { it.request.playerId == id }
```

Keep extensions in the same package as the type they extend. Don't use extensions to add unrelated behavior.

## 4. Scope Functions

| Function | Context (`this`/`it`) | Returns | Use when |
|----------|----------------------|---------|----------|
| `let` | `it` | lambda result | null checks, transformations |
| `run` | `this` | lambda result | configuring + computing result |
| `with` | `this` | lambda result | calling multiple methods on object |
| `apply` | `this` | context object | object configuration |
| `also` | `it` | context object | side effects (logging, validation) |

```kotlin
// let for null-safe chains
player?.let { connectionManager.sendToPlayer(it.id, msg) }

// apply for builder-style configuration
val config = SessionConfig().apply {
    maxPlayers = 8
    allowedVisibility = setOf(BLIND, OPEN)
}
```

## 5. Coroutine Structured Concurrency

```kotlin
// Parent scope cancels all children
coroutineScope {
    val research = async { fetchData() }    // child 1
    val analysis = async { analyze() }       // child 2
    combine(research.await(), analysis.await())
}

// supervisorScope: one child failure doesn't cancel siblings
supervisorScope {
    launch { sendToPlayer(player1, msg) }  // failure here...
    launch { sendToPlayer(player2, msg) }  // ...doesn't cancel this
}
```

## 6. StateFlow vs SharedFlow

```kotlin
// StateFlow: always has a value, conflates, replay=1
private val _state = MutableStateFlow(initialState)
val state: StateFlow<GameState> = _state.asStateFlow()

// SharedFlow: no initial value, configurable buffer/replay
private val _events = MutableSharedFlow<GameEvent>(
    replay = 0,
    extraBufferCapacity = 64,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
```

StateFlow for state holders (UI state, game state). SharedFlow for event streams (one-shot events, messages).

## 7. Data Class Patterns

```kotlin
// copy() for immutable updates
val newState = state.copy(
    players = state.players + (player.id to player),
    session = state.session.copy(currentSeq = state.session.currentSeq + 1)
)

// Destructuring
val (session, players, rolls) = gameState
```

## 8. Null Safety

```kotlin
// Elvis for defaults
val name = player?.name ?: "Unknown"

// require/check for preconditions
fun joinSession(token: AuthToken) {
    val playerId = requireNotNull(state.playerTokens[token]) { "Invalid token" }
    check(state.session.state == SessionState.LOBBY) { "Session not in lobby" }
}
```

## 9. Collection Operations

```kotlin
// associate: List → Map
val playerMap = players.associateBy { it.id }

// groupBy: List → Map<K, List<V>>
val rollsByPlayer = rolls.groupBy { it.request.playerId }

// partition: List → Pair<List, List>
val (active, expired) = effects.partition { it.isActive }

// mapNotNull: filter + map in one pass
val results = rolls.mapNotNull { it.outcome }
```

## 10. when Expressions

```kotlin
// Exhaustive matching on sealed types (compiler-enforced as expression)
val result = when (intent) {
    is GameIntent.JoinPlayer -> handleJoin(intent)
    is GameIntent.StartSession -> handleStart()
    is GameIntent.CompleteRoll -> handleRoll(intent)
    // compiler error if branch missing
}

// when with guards (Kotlin 1.9+)
when {
    player == null -> ErrorMsg("NOT_FOUND")
    player.isKicked -> ErrorMsg("KICKED")
    else -> processPlayer(player)
}
```

## 11. Inline Functions and Reified Types

```kotlin
// Reified type parameter — avoids Class<T> parameter
inline fun <reified T : GameMessage> EventLog.filterMessages(): List<T> =
    messages.filterIsInstance<T>()

// Usage: no Class argument needed
val rollResults = eventLog.filterMessages<RollResultMsg>()
```

## 12. Property Delegation

```kotlin
// lazy: computed once on first access
val parser by lazy { DiceParser() }

// Delegates.observable: react to changes
var connectionState by Delegates.observable(DISCONNECTED) { _, old, new ->
    log("Connection: $old → $new")
}
```

## 13. Companion Object Factory Methods

```kotlin
data class AuthToken(val value: String) {
    companion object {
        fun generate(): AuthToken {
            val bytes = ByteArray(32)
            SecureRandom().nextBytes(bytes)
            return AuthToken(bytes.joinToString("") { "%02x".format(it) })
        }
    }
}
```
