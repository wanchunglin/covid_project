package com.example.loginregis;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.text.method.HideReturnsTransformationMethod;
import android.text.method.PasswordTransformationMethod;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Switch;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

@SuppressLint("UseSwitchCompatOrMaterialCode")
public class register extends AppCompatActivity {
    EditText stuid;
    EditText name;
    EditText email;
    EditText phone;
    EditText password;
    Switch disp;
    ProgressBar spinner;
    Handler handler = new Handler();


    @SuppressLint("SetTextI18n")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        spinner = findViewById(R.id.progressBar7);
        name = findViewById(R.id.name);
        phone = findViewById(R.id.editTextPhone);
        email = findViewById(R.id.mail);
        stuid = findViewById(R.id.editTextNumberPassword);
        stuid.setTransformationMethod(HideReturnsTransformationMethod.getInstance());
        password = findViewById(R.id.editTextTextPassword7);
        disp = findViewById((R.id.switch3));
    }


    public void display(View view) {
        if (disp.getText().toString().equals("顯示")) {
            password.setTransformationMethod(HideReturnsTransformationMethod.getInstance());
            disp.setText("隱藏");
        } else {
            password.setTransformationMethod(PasswordTransformationMethod.getInstance());
            disp.setText("顯示");
        }
    }

    public void finish(View view) {
        String[] data = {"\"userName\": ", "\"phone\": ", "\"email\": ", "\"userID\": ", "\"password\": "};
        data[0] = data[0] + '"' + name.getText().toString() + '"';
        data[1] = data[1] + '"' + phone.getText().toString() + '"';
        data[2] = data[2] + '"' + email.getText().toString() + '"';
        data[3] = data[3] + '"' + stuid.getText().toString() + '"';
        data[4] = data[4] + '"' + password.getText().toString() + '"';

        final String registerurl = "http://140.113.79.132:8000/users/register/";

        for (int i = 0; i < 5; i++)
            Log.d(String.valueOf(i), data[i]);

        final StringBuilder content = new StringBuilder("{");

        for (int i = 0; i < 5; i++) {
            content.append(data[i]).append(", ");
        }
        content.setCharAt(content.lastIndexOf(", "), '}');

        new Thread(new Runnable() {
            @Override
            public void run() {

                handler.post(new Runnable() {
                    public void run() {
                        spinner.setVisibility(View.VISIBLE);
                    }
                });
                String response = null;
                djangocon connect = new djangocon();

                Map<String, String> property = new HashMap<>();
                property.put("Content-Type", "application/json; charset=UTF-8");
                property.put("Accept", "application/json");
                // 將資料寫入資料庫
                try {
                    response = connect.connection(registerurl, "POST", property, content.toString(), null);
                } catch (IOException e) {
                    register.this.runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(register.this, "註冊失敗請檢查網路連線", Toast.LENGTH_SHORT).show();
                        }
                    });
                    e.printStackTrace();
                    return;
                }

                try {
                    assert response != null;
                    response = new JSONObject(response).getString("status");
                } catch (JSONException e) {
                    e.printStackTrace();

                }

                if (response.contains("repeat user")) {
                    register.this.runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(register.this, "已註冊過了!", Toast.LENGTH_SHORT).show();

                        }
                    });
                } else if (response.contains("ok")) {
                    register.this.runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(register.this, "註冊成功", Toast.LENGTH_SHORT).show();
                            spinner.setVisibility(View.INVISIBLE);
                        }
                    });
                    Intent intent = new Intent();
                    intent.setClass(register.this, takephoto.class);
                    Bundle bundle = new Bundle();
                    bundle.putString("id", stuid.getText().toString());
                    intent.putExtras(bundle);
                    startActivity(intent);
                }
            }
        }).start();
    }
}