package de.agb.restapifruitshop;

import java.io.IOException;
import java.net.*;
import java.util.List;
import java.util.Scanner;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectReader;

public class ApiCall {
    protected List<Product> apiSetup() {
        URL url = null;
        try {
            url = new URI("https://api.predic8.de/shop/v2/products?start=1&limit=100").toURL();
        } catch (URISyntaxException | MalformedURLException SyntaxEx) {
            SyntaxEx.printStackTrace();
        }

        HttpURLConnection conn;

        try {
            assert url != null;
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.connect();
            int responceCode = conn.getResponseCode();
            if (responceCode != 200) {
                throw new RuntimeException("HttpResponseCode: " + responceCode);
            } else {
                StringBuilder informationString = new StringBuilder();
                Scanner scanner = new Scanner(url.openStream());

                while (scanner.hasNext()) {
                    informationString.append(scanner.nextLine());
                }

                scanner.close();

                ObjectMapper mapper = new ObjectMapper();
                JsonNode jsonNode = mapper.readTree(String.valueOf(informationString)).get("products");

                System.out.println(jsonNode);
                ObjectReader reader = mapper.readerFor(new TypeReference<List<Product>>() {
                });

                List<Product> listProducts = reader.readValue(jsonNode);

                listProducts.forEach(product ->
                        System.out.println("id: " + product.id + " name: " + product.name + " self_link: " + product.self_link)
                );

                return listProducts;

            }
        } catch (IOException ioex) {
            ioex.printStackTrace();
        }

        return null;
    }
}
