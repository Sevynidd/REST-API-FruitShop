package de.agb.restapifruitshop;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import jfxtras.styles.jmetro.JMetro;
import jfxtras.styles.jmetro.JMetroStyleClass;
import jfxtras.styles.jmetro.Style;

import java.io.IOException;
import java.util.List;
import java.util.Objects;

public class Main extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(Main.class.getResource("mainView.fxml"));
        stage.getIcons().add(new Image(
                Objects.requireNonNull(Main.class.getResourceAsStream("/images/fruits.png"))
        ));
        Scene scene = new Scene(fxmlLoader.load(), 800, 600);
        JMetro jMetro = new JMetro(Style.LIGHT);
        jMetro.setScene(scene);
        stage.setTitle("Fruit Shop");
        stage.setScene(scene);
        stage.show();

        setupView();
    }

    private void setupView() {
        ApiCall apiCall = new ApiCall();
        List<Product> listProducts = apiCall.apiSetup();



    }

    public static void main(String[] args) {
        launch();
    }
}