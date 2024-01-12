import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectReader;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.net.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ApiCall {

    private final List<Product> productList = new ArrayList<>();
    private final List<Vendor> vendorList = new ArrayList<>();

    private URL url = null;
    private HttpURLConnection conn = null;


    protected void getApiInformation() {

        try {
            url = new URI("https://api.predic8.de/shop/v2/products?limit=1000").toURL();
        } catch (URISyntaxException | MalformedURLException SyntaxEx) {
            SyntaxEx.printStackTrace();
        }

        if (url != null) {
            try {
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.connect();
                int responceCode = conn.getResponseCode();
                if (responceCode != 200) {
                    throw new RuntimeException("HttpResponseCode: " + responceCode);
                } else {
                    String informationString = "";
                    Scanner scanner = new Scanner(url.openStream());

                    while (scanner.hasNext()) {
                        informationString += scanner.nextLine();
                    }

                    scanner.close();

                    JSONObject jsonObject = new JSONObject(informationString);

                    System.out.println(jsonObject.query("/products"));

                }
            } catch (IOException ioex) {
                ioex.printStackTrace();
            }
        }
    }
}
