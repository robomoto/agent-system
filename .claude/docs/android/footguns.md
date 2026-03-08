# Android / Jetpack Compose Footguns

Version: Compose 1.6+ / Material3 / minSdk 26+

## 1. Recomposition Executes Composables Arbitrarily

Compose may re-execute any composable at any time. Side effects in the composable body will re-run:

```kotlin
// BAD: logs on every recomposition
@Composable
fun PlayerCard(player: Player) {
    Log.d("TAG", "Rendering ${player.name}")  // fires repeatedly
    Text(player.name)
}

// GOOD: use SideEffect for non-Compose side effects
@Composable
fun PlayerCard(player: Player) {
    SideEffect { Log.d("TAG", "Rendering ${player.name}") }
    Text(player.name)
}
```

## 2. remember{} Lost on Configuration Change

`remember {}` survives recomposition but NOT configuration changes (rotation, dark mode toggle, locale change). User input stored in `remember` disappears.

```kotlin
// BAD: dice expression lost on rotation
val expression = remember { mutableStateOf("") }

// GOOD: survives configuration change
val expression = rememberSaveable { mutableStateOf("") }

// BEST: store in ViewModel (survives config change + process death with SavedStateHandle)
```

## 3. LaunchedEffect Key Mistakes

```kotlin
// BAD: key=Unit means effect runs ONCE, even if playerId changes
LaunchedEffect(Unit) {
    loadPlayerData(playerId)  // stale playerId after navigation
}

// GOOD: re-run when playerId changes
LaunchedEffect(playerId) {
    loadPlayerData(playerId)
}

// BAD: key=state (entire object) — effect restarts on every state change
LaunchedEffect(state) { /* restarts too often */ }

// GOOD: key on specific field that should trigger restart
LaunchedEffect(state.isKicked) { /* only when kicked status changes */ }
```

## 4. viewModelScope Cancels on ViewModel.onCleared()

Coroutines in `viewModelScope` are cancelled when the ViewModel is cleared (Activity destroyed, NavBackStackEntry popped). For the DM server, this is correct — server should stop when DM leaves. But for background work that should outlive the screen (uploading data, saving state), use a separate scope or WorkManager.

## 5. Room Main Thread Crashes

Room throws `IllegalStateException` if you run a query on the main thread (unless `.allowMainThreadQueries()` is set, which you should never do in production).

```kotlin
// BAD: crashes on main thread
fun getSession(id: String) = dao.getById(id)

// GOOD: suspend function
suspend fun getSession(id: String) = dao.getById(id)

// GOOD: reactive Flow (collected on main, executed on Room's dispatcher)
fun observeSessions(): Flow<List<Session>> = dao.getAll()
```

## 6. Room Entity Default Parameters

Room uses reflection to instantiate entities. If your data class has default parameters, Room may not use them — it looks for a no-arg constructor or a constructor matching column names.

```kotlin
// RISKY: Room might not use these defaults
@Entity data class RollEntity(
    @PrimaryKey val id: String,
    val total: Int = 0,        // Room may ignore this default
    val label: String = ""     // and this one
)
```

**Fix**: Ensure all columns are present in queries, or use `@ColumnInfo(defaultValue = "0")` for database-level defaults.

## 7. NSD Callbacks on System Threads

`NsdManager` callbacks (`onServiceFound`, `onServiceResolved`, etc.) run on system binder threads, NOT the main thread. Updating UI state from these callbacks requires dispatching to the main thread.

```kotlin
// BAD: updating MutableStateFlow from binder thread is technically safe
// (StateFlow is thread-safe) but violating Android threading conventions

// GOOD: explicit main thread dispatch
override fun onServiceFound(serviceInfo: NsdServiceInfo) {
    mainScope.launch { _discoveredSessions.update { it + serviceInfo } }
}
```

## 8. NavController.navigate() During Composition

```kotlin
// BAD: may crash or navigate multiple times
@Composable
fun Screen(state: State) {
    if (state.isDone) {
        navController.navigate("home")  // called during composition!
    }
}

// GOOD: use LaunchedEffect
LaunchedEffect(state.isDone) {
    if (state.isDone) navController.navigate("home")
}
```

## 9. collectAsState vs collectAsStateWithLifecycle

```kotlin
// BAD: keeps collecting when app is in background
val state by flow.collectAsState()

// GOOD: stops collecting when lifecycle is below STARTED
val state by flow.collectAsStateWithLifecycle()
```

`collectAsState` can cause crashes if the flow emits something that triggers UI work while the app is backgrounded (e.g., FragmentManager operations).

## 10. Modifier.clickable Without Indication

```kotlin
// BAD: clickable but no visual feedback (no ripple)
Modifier.clickable { onClick() }

// GOOD: explicit ripple indication (default since Compose 1.7)
// In Compose 1.7+, clickable includes ripple by default
// For older versions:
Modifier.clickable(
    interactionSource = remember { MutableInteractionSource() },
    indication = rememberRipple()
) { onClick() }
```

## 11. enableEdgeToEdge() Without Insets Handling

After `enableEdgeToEdge()`, content draws behind system bars. Without proper insets handling, content goes under the status bar and navigation bar.

```kotlin
// Scaffold handles this automatically:
Scaffold { innerPadding ->
    Column(Modifier.padding(innerPadding)) { /* safe */ }
}

// Without Scaffold, handle manually:
Column(Modifier.windowInsetsPadding(WindowInsets.systemBars)) { /* safe */ }
```

## 12. Compose Preview Limitations

`@Preview` composables cannot:
- Access ViewModels (no ViewModelStoreOwner)
- Use `collectAsStateWithLifecycle` (no lifecycle owner)
- Call `LocalContext.current` for real Android operations

Always create stateless preview composables with hardcoded sample data.
