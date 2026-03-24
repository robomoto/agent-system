<!-- last_verified: 2026-03-07 -->
# Android Reference — Key APIs

Version: Compose 1.6+ / Material3 1.2+ / Room 2.6+ / Navigation 2.7+

## Jetpack Compose Core

### State
- `remember { mutableStateOf(value) }` — local recomposition-surviving state
- `rememberSaveable { mutableStateOf(value) }` — survives configuration changes
- `derivedStateOf { computation }` — computed state that only triggers recomposition when result changes
- `snapshotFlow { state.value }` — convert Compose state to Flow

### Side Effects
- `LaunchedEffect(key) { }` — run suspend code, restart when key changes
- `DisposableEffect(key) { onDispose { } }` — register/unregister pattern
- `SideEffect { }` — every successful recomposition
- `rememberCoroutineScope()` — get scope for event handlers (onClick, etc.)
- `rememberUpdatedState(value)` — capture latest value in long-running effects

### Animation
- `AnimatedContent(targetState) { state -> }` — animate between different content
- `AnimatedVisibility(visible) { }` — animate show/hide
- `animateContentSize()` — animate size changes
- `Crossfade(targetState) { state -> }` — simple fade transition

### Layout
- `Scaffold` — top bar, bottom bar, FAB, content with proper insets
- `Column`, `Row`, `Box` — basic layout
- `LazyColumn`, `LazyRow` — recycling lists
- `ModalBottomSheet` — bottom sheet overlay

## Material3

### Components
- `TopAppBar(title, navigationIcon, actions)` — app bar
- `Card(onClick) { }` — clickable card
- `FilledTonalButton(onClick) { }` — secondary emphasis button
- `OutlinedTextField(value, onValueChange, label)` — text input
- `AlertDialog(onDismissRequest, title, text, confirmButton, dismissButton)`
- `FilterChip(selected, onClick, label)` — toggleable chip
- `CircularProgressIndicator()` — loading spinner
- `Snackbar` / `SnackbarHost` — transient messages
- `IconButton(onClick) { Icon() }` — icon-only button

### Theming
```kotlin
MaterialTheme(
    colorScheme = darkColorScheme(
        primary = Color(0xFF4FC3F7),
        surface = Color(0xFF1C2B3A),
        // ...
    ),
    typography = Typography(/* ... */)
) { content() }
```

- `MaterialTheme.colorScheme.primary` — access theme colors
- `MaterialTheme.typography.bodyMedium` — access text styles

## Navigation Compose

```kotlin
// Define nav graph
NavHost(navController, startDestination = "home") {
    composable("home") { HomeScreen() }
    composable("dm/{sessionId}", arguments = listOf(navArgument("sessionId") { type = NavType.StringType })) {
        DmScreen()
    }
}

// Navigate
navController.navigate("dm/$sessionId")
navController.navigate("home") { popUpTo("home") { inclusive = true }; launchSingleTop = true }
navController.popBackStack()
```

## Room

### Database
```kotlin
@Database(entities = [SessionEntity::class, RollEntity::class], version = 1)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun sessionDao(): SessionDao
}
```

### TypeConverters
```kotlin
class Converters {
    @TypeConverter fun fromJson(value: String): List<String> = Json.decodeFromString(value)
    @TypeConverter fun toJson(value: List<String>): String = Json.encodeToString(value)
}
```

### Building
```kotlin
Room.databaseBuilder(context, AppDatabase::class.java, "blind-roll-db")
    .fallbackToDestructiveMigration()  // OK for dev; use migrations in production
    .build()
```

## ViewModel

```kotlin
class MyViewModel(private val repo: MyRepository) : ViewModel() {
    private val _state = MutableStateFlow(MyState())
    val state: StateFlow<MyState> = _state.asStateFlow()

    fun doAction() {
        viewModelScope.launch {
            val result = repo.fetch()
            _state.update { it.copy(data = result) }
        }
    }
}
```

## Android Platform

### NSD (Network Service Discovery)
```kotlin
val serviceInfo = NsdServiceInfo().apply {
    serviceName = "BlindRoll_$roomCode"
    serviceType = "_blindroll._tcp."
    port = serverPort
}
nsdManager.registerService(serviceInfo, NsdManager.PROTOCOL_DNS_SD, registrationListener)
nsdManager.discoverServices("_blindroll._tcp.", NsdManager.PROTOCOL_DNS_SD, discoveryListener)
```

### BackHandler
```kotlin
BackHandler(enabled = shouldIntercept) {
    // handle back press
}
```

### Edge-to-Edge
```kotlin
// In Activity.onCreate(), before setContent:
enableEdgeToEdge()
```

### Haptic Feedback
```kotlin
val view = LocalView.current
view.performHapticFeedback(HapticFeedbackConstants.CONFIRM)
view.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP)
```

## OkHttp WebSocket

```kotlin
val client = OkHttpClient.Builder()
    .pingInterval(30, TimeUnit.SECONDS)
    .build()

val request = Request.Builder().url("ws://host:port/ws?token=$token").build()
client.newWebSocket(request, object : WebSocketListener() {
    override fun onMessage(webSocket: WebSocket, text: String) { /* ... */ }
    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) { /* ... */ }
    override fun onClosing(webSocket: WebSocket, code: Int, reason: String) { /* ... */ }
})
```

## Ktor Server (Embedded)

```kotlin
embeddedServer(CIO, port = 0) {
    install(WebSockets)
    install(ContentNegotiation) { json() }
    routing {
        get("/session/{code}") { /* ... */ }
        webSocket("/ws") { /* ... */ }
    }
}.start(wait = false)
```
