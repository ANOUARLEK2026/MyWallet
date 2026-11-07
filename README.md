# MyWallet for Android (v6)

## New in v6: redesigned home + much richer Settings
Inspired by Monefy, Money Manager, Wallet (BudgetBakers), Spendee, YNAB and Mint.
- **Home screen:** month/year navigator (browse past periods), balance hero with 14-day spending sparkline and available cash, **Safe-to-spend today** (daily allowance from your budgets, YNAB/Mint style), **Favorites** (one-tap templates), **Accounts strip**, smart alerts, category donut with icons, **Budgets** progress, **Recent transactions**, **Goals**. Everything can be hidden/reordered: Settings → Customize home.
- **Hide balances:** 👁 button in the header (or Settings) blurs all amounts.
- **Favorites / templates:** create from the home screen, Settings, or ★ inside any transaction; tap to log instantly (with Undo).
- **Categories manager:** emoji icon + color for every category, create/rename/delete your own categories.
- **Settings:** name (greeting), theme (auto/light/dark), 6 accent colors, text size, category icons, default start screen, compact quick-add bar, decimals on/off, first day of week (calendar + weekly reports), haptics, per-type alert switches, bill reminder lead time, report banner, backup reminder (weekly/monthly), shortcuts to categories/templates/income sources/recurring. Settings are saved in the JSON backup.

# MyWallet for Android (v5)

## New in v5: smart layer
- **Plan → Forecast:** projected balance at the end of the month (current cash + scheduled income − scheduled bills − your average variable daily spending), with range, daily path chart, and a warning with the expected date if cash may run out.
- **Stats → Smart analysis:** plain-language insights, where the money goes (with change vs previous period), top payees/notes, spending rhythm, small repeated expenses, unusual transactions, saving opportunities. (Rule-based, runs 100% offline; not an AI model.)
- **Stats → Compare:** this month vs last (same days), full months, 30 days, week, year, or any two months; per-category changes.
- **Recurring:** weekly / biweekly / monthly / quarterly / yearly, end date, pause, edit. Old rules keep working without duplicates.
- **Stats → Reports:** weekly (Sat-Fri), monthly, yearly reports with navigation; share as text or save as HTML/PDF; a "report is ready" card appears on the dashboard.
- **Plan → Income:** multiple income sources with expected amount/day, share, stability and diversification. Assign a source in quick-add (+), edit sheet, or bulk.
- **Plan → Subscriptions:** monthly/yearly cost, renewal dates with reminders, pause, and automatic detection of repeating expenses in your history.
- **History → Calendar:** month grid with spending heat, income dots and upcoming due dates; tap a day to see/add.
- **Smart alerts (dashboard):** budget at 70/80/90% (Settings), pace-based budget warning, bills & renewals due soon, weekly spending spike, unusual transactions, cash-out risk. Shown in-app; no notification permission needed.
- **Tags:** type `#tag` in the note field (e.g. `lunch #work`), edit on a transaction, bulk-tag in History (long-press → Tag), filter by tag, tag totals/rename/merge/delete in Stats → Tags. CSV has Tags and Source columns.
- New data (sources, alert setting) is included in backups, snapshots and Undo.


## New in v4: full financial picture
- **Wealth tab:** net worth (assets minus debts) with monthly history, accounts with transfers, assets (property, gold, shares…) with gain/loss, debts and money owed to you with Pay buttons, savings goals with monthly-needed and ETA.
- **Plan tab:** 1 to 5 year forecast with what-if sliders (income, spending, asset growth, one-off expense), cash-out warning, next-30-days bills, financial health score (0-100) with advice, budgets and recurring items.
- **Tools:** can-I-afford-it, loan calculator, investment growth with inflation, retirement planner (4% rule), 50/30/20 check, debt payoff (avalanche vs snowball).
- Backups, undo and snapshots cover all of the above.

Same features as MyWallet 2.2 for Windows (quick-add with smart amounts, history with search/filters/bulk edit,
dashboard with period comparison, statistics, budgets, recurring items, undo, dark/light, CSV import/export,
JSON backup/restore, auto-snapshots), redesigned for one-handed phone use. 100% offline; data stays on the phone.

## Fastest: install as an app (no APK needed)
1. Put the `www` folder on any HTTPS host (GitHub Pages, Netlify drop, Cloudflare Pages — all free).
2. Open the link in Chrome on your phone → menu ⋮ → **Install app**.

## Real APK (no Android Studio needed)
1. Create a GitHub repo and upload this whole folder.
2. Actions tab → **Build MyWallet APK** → Run. About 4 minutes later download `MyWallet-apk` → `app-debug.apk`.
3. Copy to the phone, open it, allow "install unknown apps".
(With Android Studio: `npm install && npx cap add android && npx cap sync && npx cap open android`.)

## Moving your Windows data
Windows MyWallet → Export → **CSV**. On the phone: More → **Import CSV**. Duplicates are skipped.

## Using it
- Type an amount and press **Add**. `12k`, `1.5m`, `800+250`, `3*450` all work. Start with `+` for income.
- Long-press a transaction to multi-select (set category / type / delete). Tap to edit or duplicate.
- Every change has an **Undo** in the toast.

## النسخة العربية (RTL)
واجهة عربية كاملة من اليمين لليسار. الترجمة في `www/ar.js` (قاموس + مترجم تلقائي)، وتبقى البيانات المخزّنة بمفاتيحها الإنجليزية لتبقى النسخ الاحتياطية وملفات CSV القديمة متوافقة. لإضافة ترجمة نص جديد أضف سطراً `English|عربي` في القاموس.

## App lock (fingerprint)
More → **App lock** turns on fingerprint unlock (the phone's PIN/pattern is the fallback). Options: lock after (immediately / 30 s / 1 min / 5 min) and *Hide in recent apps* (also blocks screenshots). Turning the lock on or off asks for your fingerprint first.
Native code lives in `native/` and is copied into the Android project by `scripts/apply-native.sh` (already run on `android/`, and run automatically by the GitHub workflow). If you regenerate `android/` yourself, run `bash scripts/apply-native.sh` after `npx cap sync`.
Works only in the APK; in the browser/PWA the switch is disabled.
