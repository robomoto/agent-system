# Android / Jetpack Compose Idioms

Version: Compose 1.6+ / Material3 / minSdk 26+

## 1. State Hoisting (State Up, Events Down)

```kotlin
// Stateless composable — receives state, emits events
@Composable
fun PlayerScreen(
    state: PlayerState,           // state flows down
    onRoll: (String) -> Unit,     // events flow up
    onLeave: () -> Unit
) { /* ... */ }

// Stateful wrapper — connects to ViewModel
@Composable
fun PlayerScreenRoute(viewModel: PlayerViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    PlayerScreen(state = state, onRoll = viewModel::roll, onLeave = viewModel::leave)
}
```

## 2. remember vs rememberSaveable

```kotlin
// remember: survives recomposition, LOST on configuration change
val expanded = remember { mutableStateOf(false) }

// rememberSaveable: survives configuration change (rotation, theme toggle)
val diceExpression = rememberSaveable { mutableStateOf("1d20") }
```

Use `rememberSaveable` for user input and UI state that should survive rotation. Use `remember` for derived/computed values.

## 3. Side Effects

| Effect | When it runs | Use for |
|--------|-------------|---------|
| `LaunchedEffect(key)` | On enter + when key changes | One-shot operations, flow collection |
| `DisposableEffect(key)` | On enter + when key changes, with cleanup | Registering/unregistering listeners |
| `SideEffect` | After every successful recomposition | Syncing Compose state to non-Compose code |

```kotlin
// LaunchedEffect: navigate on state change
LaunchedEffect(state.isKicked) {
    if (state.isKicked) { navController.navigate("home") }
}

// DisposableEffect: register NSD, clean up on leave
DisposableEffect(Unit) {
    nsdManager.registerService(serviceInfo, protocol, listener)
    onDispose { nsdManager.unregisterService(listener) }
}
```

## 4. ViewModel + StateFlow

```kotlin
class DmViewModel(private val gameSession: GameSession) : ViewModel() {
    private val _state = MutableStateFlow(DmState())
    val state: StateFlow<DmState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            gameSession.state.collect { gameState ->
                _state.update { it.copy(gameState = gameState) }
            }
        }
    }
}
```

## 5. collectAsStateWithLifecycle

```kotlin
// GOOD: stops collecting when app is backgrounded
val state by viewModel.state.collectAsStateWithLifecycle()

// BAD: keeps collecting in background (wasted resources)
val state by viewModel.state.collectAsState()
```

Requires `androidx.lifecycle:lifecycle-runtime-compose`.

## 6. Navigation Compose

```kotlin
NavHost(navController, startDestination = "home") {
    composable("home") { HomeScreen(onNavigate = { navController.navigate(it) }) }
    composable("dm/{sessionId}") { backStackEntry ->
        val sessionId = backStackEntry.arguments?.getString("sessionId")
        DmScreen(sessionId = sessionId!!)
    }
}

// Navigate with flags
navController.navigate("home") {
    popUpTo("home") { inclusive = true }  // clear backstack
    launchSingleTop = true                // avoid duplicate
}
```

## 7. Room Patterns

```kotlin
@Entity(tableName = "sessions")
data class SessionEntity(
    @PrimaryKey val id: String,
    val name: String,
    val createdAt: Long,
    @ColumnInfo(name = "dm_player_id") val dmPlayerId: String
)

@Dao
interface SessionDao {
    @Query("SELECT * FROM sessions ORDER BY createdAt DESC")
    fun getAll(): Flow<List<SessionEntity>>  // reactive

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(session: SessionEntity)  // one-shot
}
```

## 8. Manual DI with AppContainer

```kotlin
class AppContainer(private val context: Context) {
    val database by lazy { Room.databaseBuilder(context, AppDatabase::class.java, "blind-roll").build() }
    val sessionRepository by lazy { SessionRepository(database.sessionDao()) }
    // ... other dependencies
}

// Access from Activity
val container = (application as BlindRollApp).container
```

No Hilt/Dagger/Koin overhead. Works well for <20 dependencies.

## 9. BackHandler

```kotlin
// Intercept system back button
BackHandler(enabled = isSessionActive) {
    showEndSessionDialog = true
}
```

When `enabled = false`, falls through to NavController's default back handling.

## 10. Material3 TopAppBar with Navigation

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScreenWithBackNav(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Screen Title") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                }
            )
        }
    ) { padding -> /* content */ }
}
```

## 11. Edge-to-Edge + WindowInsets

```kotlin
// In Activity.onCreate()
enableEdgeToEdge()

// In Compose — Scaffold handles insets automatically via padding parameter
Scaffold { innerPadding ->
    Column(modifier = Modifier.padding(innerPadding)) { /* content */ }
}
```

## 12. Modifier Ordering

Order matters! Modifiers apply outside-in:
```kotlin
Modifier
    .padding(16.dp)        // space outside the background
    .background(color)     // background drawn in padded area
    .clip(RoundedCornerShape(8.dp))  // clip after background
    .clickable { }         // click area includes padding
```

## 13. AnimatedContent / AnimatedVisibility

```kotlin
// Animate between different content states
AnimatedContent(targetState = rollState, label = "roll") { state ->
    when (state) {
        is Pending -> Text("?")
        is Revealed -> Text("${state.total}")
    }
}

// Show/hide with animation
AnimatedVisibility(visible = isExpanded) {
    ExpandedContent()
}
```
