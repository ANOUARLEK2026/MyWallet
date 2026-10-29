package com.mywallet.app;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;

import androidx.activity.result.ActivityResult;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.ActivityCallback;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/**
 * Lets the user choose where a file is saved (Downloads, Documents, Drive, SD card ...)
 * using Android's system "Save as" screen (Storage Access Framework).
 * No storage permission is needed.
 *
 * JS: Capacitor.Plugins.FileSaver.saveFile({ name, mime, data })
 *     -> { saved: true, uri }  or  { saved: false, cancelled: true }
 */
@CapacitorPlugin(name = "FileSaver")
public class FileSaverPlugin extends Plugin {

    @PluginMethod
    public void saveFile(PluginCall call) {
        String name = call.getString("name");
        String data = call.getString("data");
        String mime = call.getString("mime");
        if (name == null || name.isEmpty() || data == null) {
            call.reject("name and data are required");
            return;
        }
        if (mime == null || mime.isEmpty()) {
            mime = "application/octet-stream";
        }
        Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType(mime);
        intent.putExtra(Intent.EXTRA_TITLE, name);
        try {
            startActivityForResult(call, intent, "onSaveResult");
        } catch (Exception e) {
            call.reject("Cannot open the save dialog: " + e.getMessage());
        }
    }

    @ActivityCallback
    private void onSaveResult(PluginCall call, ActivityResult result) {
        if (call == null) {
            return;
        }
        Intent intent = result.getData();
        if (result.getResultCode() != Activity.RESULT_OK || intent == null || intent.getData() == null) {
            JSObject cancelled = new JSObject();
            cancelled.put("saved", false);
            cancelled.put("cancelled", true);
            call.resolve(cancelled);
            return;
        }
        Uri uri = intent.getData();
        String data = call.getString("data");
        try (OutputStream out = getContext().getContentResolver().openOutputStream(uri, "wt")) {
            if (out == null) {
                call.reject("Could not open the chosen file");
                return;
            }
            out.write(data.getBytes(StandardCharsets.UTF_8));
            out.flush();
            JSObject ok = new JSObject();
            ok.put("saved", true);
            ok.put("uri", uri.toString());
            call.resolve(ok);
        } catch (Exception e) {
            call.reject("Could not write the file: " + e.getMessage());
        }
    }
}
