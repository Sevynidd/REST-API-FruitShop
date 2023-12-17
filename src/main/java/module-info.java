module de.agb.restapifruitshop {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires com.fasterxml.jackson.databind;
    requires org.jfxtras.styles.jmetro;

    opens de.agb.restapifruitshop to javafx.fxml;
    exports de.agb.restapifruitshop;
}