# Variant: Mobile app (Flutter — adapt for React Native)

Paste these into the matching sections of `AGENTS.md`.

## 3. Stack and layout

- **Framework:** Flutter (Dart) <or React Native — say which>
- **State management:** <Riverpod | Bloc | Provider>
- **Tests:** `flutter_test` (widget + unit), <integration_test>
- **Backend:** <API this app talks to>

```
lib/
  features/<name>/   screen, widgets, controller, tests
  core/              theme, routing, api client
test/
docs/                prd.md, adr/
```

## 4. Commands

| Purpose | Command |
| --- | --- |
| Install | `flutter pub get` |
| Run | `flutter run` |
| Test | `flutter test` |
| Test one file | `flutter test test/<path>` |
| Lint | `flutter analyze` |
| Format | `dart format .` |
| Build | `flutter build <apk\|ios>` |

## 5. Conventions — additions

- Widgets are presentational; logic lives in the controller/state layer and is unit tested without a widget tree.
- Every screen handles loading, empty, error, and offline states.
- No hardcoded strings or colors in widgets — use the theme and the localization file.
- Respect platform differences where they matter (back navigation, safe areas, permissions dialogs).
- Test on both a small phone and a tablet width before calling a screen done.

## 7. Guardrails — additions

- **App binaries can be decompiled.** No API keys, secrets, or credentials in the app code, ever.
- Never request a new device permission (camera, location, contacts, notifications) without approval — it changes the store listing and user trust.
- Never change bundle id, signing config, entitlements, or store metadata.
- Never add an SDK that collects analytics or user data without approval.
