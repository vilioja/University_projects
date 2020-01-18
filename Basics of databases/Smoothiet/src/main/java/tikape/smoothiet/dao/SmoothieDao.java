package tikape.smoothiet.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import tikape.smoothiet.database.Database;
import tikape.smoothiet.domain.Smoothie;

public class SmoothieDao implements Dao<Smoothie, Integer> {

    private Database database;

    public SmoothieDao(Database database) {
        this.database = database;
    }

    @Override
    public Smoothie etsiYksi(Integer key) throws SQLException {

        Smoothie smoothie = new Smoothie();

        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT * FROM Smoothie WHERE id = ?");
            stmt.setInt(1, key);
            ResultSet result = stmt.executeQuery();

            while (result.next()) {
                smoothie = new Smoothie(result.getInt("id"), result.getString("nimi"));
            }
        }

        return smoothie;
    }

    @Override
    public List<Smoothie> etsiKaikki() throws SQLException {
        List<Smoothie> smoothiet = new ArrayList<>();

        try (Connection conn = database.getConnection()) {
            ResultSet result = conn.prepareStatement("SELECT id, nimi FROM Smoothie").executeQuery();

            while (result.next()) {
                smoothiet.add(new Smoothie(result.getInt("id"), result.getString("nimi")));
            }
        }

        return smoothiet;
    }

    @Override
    public Smoothie tallenna(Smoothie object) throws SQLException {
        Smoothie nimella = etsiNimella(object.getNimi());

        if (nimella != null) {
            return nimella;
        }

        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO Smoothie (nimi) VALUES (?)");
            stmt.setString(1, object.getNimi());
            stmt.executeUpdate();
        }

        return etsiNimella(object.getNimi());
    }

    private Smoothie etsiNimella(String nimi) throws SQLException {
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT * FROM Smoothie WHERE nimi = ?");
            stmt.setString(1, nimi);

            ResultSet result = stmt.executeQuery();
            if (!result.next()) {
                return null;
            }

            return new Smoothie(result.getInt("id"), result.getString("nimi"));
        }
    }

    @Override
    public void poista(Integer key) throws SQLException {
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt1 = conn.prepareStatement("DELETE FROM SmoothieAinesosa WHERE smoothie_id = ?");
            stmt1.setInt(1, key);
            stmt1.executeUpdate();

            PreparedStatement stmt2 = conn.prepareStatement("DELETE FROM Smoothie WHERE id = ?");
            stmt2.setInt(1, key);
            stmt2.executeUpdate();
        }
    }

}
