package com.example.koru.t11_pren1;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.util.TypedValue;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.TreeMap;
import java.util.UUID;

public class MainActivity extends AppCompatActivity{
    private TextView txtRecMsg;
    private TextView txtStatus;
    private TextView txtSteps;
    private Button cmdStart;
    private Button cmdConnect;

    private BluetoothAdapter btAdapter;
    private BluetoothDevice device;

    private BluetoothSocket btSocket;
    private AsyncTask<BluetoothSocket, Void, String> readerTask;

    private boolean errorDetected = false;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onDestroy() {
        readerTask.cancel(true);

        String message = "disconnect";

        try {
            OutputStream oStream = btSocket.getOutputStream();
            oStream.write(message.getBytes());
            oStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

        super.onDestroy();
    }

    public void startProcess(View o) {
        if (!btSocket.isConnected()) { System.out.println("no connection"); return; }
        int steps_in_mm = Integer.parseInt(txtSteps.getText().toString());
        System.out.println("Value in mm: " + steps_in_mm);
        String message = "start-process@" + convert_mm_to_steps(steps_in_mm);
        System.out.println("Value in steps: " + message);

        try {
            OutputStream oStream = btSocket.getOutputStream();
            oStream.write(message.getBytes());
            oStream.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }

        cmdStart.setEnabled(false);
    }

    public void connectBT(View o) {
        Log.d("Method", "OK");

        txtRecMsg = (TextView)findViewById(R.id.txtRecMessage);
        txtStatus = (TextView)findViewById(R.id.txtStatus);
        txtSteps = (TextView)findViewById(R.id.txtSteps);
        cmdStart = (Button)findViewById(R.id.cmdStartProcess);
        cmdConnect = (Button)findViewById(R.id.cmdConnect);

        btAdapter = BluetoothAdapter.getDefaultAdapter();

        Log.d("Bluetoothadapter", btAdapter.getName());
        device = btAdapter.getBondedDevices().iterator().next();

        Log.d("Device", "Got bonded device: " + device);

        try {
            btSocket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001105-0000-1000-8000-00805f9b34fb"));
            btAdapter.cancelDiscovery();

            Log.d("Socket", "Socket created:" + btSocket);
            txtStatus.setText("Status: Establishing connection...");
            try {
                btSocket.connect();
                Log.e("","Connected");
            } catch (IOException e) {
                Log.e("",e.getMessage());

                try {
                    Log.e("","trying fallback...");

                    btSocket =(BluetoothSocket) device.getClass().getMethod("createRfcommSocketToServiceRecord", new Class[] {int.class}).invoke(device,1);
                    btSocket.connect();

                    Log.e("","Connected");
                }
                catch (Exception e2) {
                    Log.e("", "Couldn't establish Bluetooth connection!");
                }
            }

            if (btSocket.isConnected()) {
                Log.d("ReaderTask", "Starting reader...");
                readerTask = new BluetoothReader().execute(btSocket);
                txtStatus.setText("Status: Connected to robot");
                cmdStart.setEnabled(true);
                cmdConnect.setEnabled(false);
            } else {
                txtStatus.setText("Status: Failed to connect to robot");
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    private int convert_mm_to_steps(float mm) {
        float y = mm / 10f;
        return (int) Math.round(-100*(Math.sqrt(-1000*(y - 2215.269))-1480));
    }

    private float convert_steps_to_mm(int steps) {
        return (float) (2215.269 + (Math.pow(1480 + steps / -100, 2) / -1000));
    }

    private float recalculateDistance(float distance) {
        return distance / 10;
    }

    private float convert_mm_to_pixels(float mm) {
        return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_MM, 1,
                getResources().getDisplayMetrics()) * mm;
    }

    private class BluetoothReader extends AsyncTask<BluetoothSocket, Void, String>  {
        @Override
        protected String doInBackground(BluetoothSocket... params) {
            BluetoothSocket btSocket = params[0];
            InputStream iStream;
            int iMsg;
            String sMsg = "";

            try {
                Log.d("BluetoothReader", "Is connected:" + btSocket.isConnected());
                while (!errorDetected) {
                    iStream = btSocket.getInputStream();

                    while((iMsg = iStream.read())!=-1) {
                        // converts integer to character
                        char charMsg = (char)iMsg;

                        if (charMsg != '#') {
                            sMsg += charMsg;
                        } else {
                            return sMsg;
                        }
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                errorDetected = true;
            }

            return "";
        }

        @Override
        protected void onPostExecute(String s) {
            Log.d("BluetoothReader", "Received message from server: " + s);

            if (s.contains("status") && s.contains("started")) {
                cmdStart.setEnabled(false);
            } else if (s.toLowerCase().contains("position")) {
                String[] arrSplitter = s.split("@");
                String[] arrMessage = arrSplitter[1].split(";");

                int stepsX = Integer.parseInt(arrMessage[1]);
                int stepsY = Integer.parseInt(arrMessage[2]);
                float distanceX = convert_steps_to_mm(stepsX);
                float distanceY = convert_steps_to_mm(stepsY);
                float downscaledX = recalculateDistance(distanceX);
                float downscaledY = recalculateDistance(distanceY);
                float pixelsX = convert_mm_to_pixels(downscaledX);
                float pixelsY = convert_mm_to_pixels(downscaledY);

                txtRecMsg.setText("Received position: X " + arrMessage[1] + ", Y " + arrMessage[2]);
            }

            readerTask = new BluetoothReader().execute(btSocket);
        }
    }
}
