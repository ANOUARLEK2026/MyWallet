# MyWallet for Android (v4.1)

## New in v4.1
- **App icon:** the launcher icon is now `App.png` (adaptive icon for Android 8+, plus legacy and round icons). To change it later, replace `App.png` and run `python3 tools/make_icons.py`.
- **Password login:** the app asks for a password every time it opens (and after it has been in the background longer than the Auto-lock time). First launch: create a password and save the **recovery code** shown once. Settings → **Security**: change password, new recovery code, auto-lock time, lock now. Only a salted hash is stored, in its own key, so backups and "Clear" never touch it.
- **Backup / exports you can find:** Backup, CSV export and the report now open Android's own **Save as** screen, so you choose the folder (Downloads, Documents, Drive...). The report is saved as an `.html` file: open it in a browser and print to PDF.
- **Stable signing key:** every APK built by the workflow is signed with `android-keystore/debug.keystore`, so a new APK installs over the old one and keeps your data. (Debug key, for personal use.)

## Build the APK
1. Upload this whole folder to a GitHub repo.
2. Actions tab → **Build MyWallet APK** → Run → download `MyWallet-apk` → `app-debug.apk`.
3. With Android Studio instead: `npm install && npx cap add android && bash scripts/android-customize.sh && npx cap sync android && npx cap open android`.

**Important before installing over an older build:** first make a backup in the old app. If Android says "App not installed" the old build was signed with a different key; uninstalling would delete its data.

**Forgot the password?** Use "Forgot password?" on the lock screen with your recovery code. With neither, reinstall the app and restore a backup file.

# MyWallet for Android (v4)

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
