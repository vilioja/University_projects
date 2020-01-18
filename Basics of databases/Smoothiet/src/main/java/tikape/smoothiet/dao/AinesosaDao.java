
package tikape.smoothiet.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import tikape.smoothiet.database.Database;
import tikape.smoothiet.domain.Ainesosa;


public class AinesosaDao implements Dao<Ainesosa, Integer> {

    private Database database;

    public AinesosaDao(Database database) {
        this.database = database;
    }
    
    @Override
    public Ainesosa etsiYksi(Integer key) throws SQLException {
        Ainesosa ainesosa = new Ainesosa();
        
        try (Connection conn = database.getConnection()) {
                PreparedStatement stmt = conn.prepareStatement("SELECT * FROM Ainesosa WHERE id = ?");
                stmt.setInt(1, key);
                ResultSet result = stmt.executeQuery();
                
            while (result.next()) {
                ainesosa = new Ainesosa(result.getInt("id"), result.getString("nimi"), result.getString("allergeeni"));
            }
        }
        
        return ainesosa;
    }

    @Override
    public List<Ainesosa> etsiKaikki() throws SQLException {
        List<Ainesosa> ainesosat = new ArrayList<>();

        try (Connection conn = database.getConnection()) {
                ResultSet result = conn.prepareStatement("SELECT * FROM Ainesosa").executeQuery();

            while (result.next()) {
                ainesosat.add(new Ainesosa(result.getInt("id"), result.getString("nimi"), result.getString("allergeeni")));
            }
        }

        return ainesosat;
    }

    @Override
    public Ainesosa tallenna(Ainesosa object) throws SQLException {
        Ainesosa nimella = etsiNimella(object.getNimi());

        if (nimella != null) {
            return nimella;
        }

        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO Ainesosa (nimi, allergeeni) VALUES (?,?)");
            stmt.setString(1, object.getNimi());
            stmt.setString(2, object.getAllergeeni());
            stmt.executeUpdate();
        }

        return etsiNimella(object.getNimi());
    }
    
    private Ainesosa etsiNimella(String nimi) throws SQLException {
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT * FROM Ainesosa WHERE nimi = ?");
            stmt.setString(1, nimi);

            ResultSet result = stmt.executeQuery();
            if (!result.next()) {
                return null;
            }

            return new Ainesosa(result.getInt("id"), result.getString("nimi"), result.getString("allergeeni"));
        }
    }

    @Override
    public void poista(Integer key) throws SQLException {
        try (Connection conn = database.getConnection()) {
                PreparedStatement stmt1 = conn.prepareStatement("DELETE FROM SmoothieAinesosa WHERE ainesosa_id = ?");
                stmt1.setInt(1, key);
                stmt1.executeUpdate();
            
                PreparedStatement stmt2 = conn.prepareStatement("DELETE FROM Ainesosa WHERE id = ?");
                stmt2.setInt(1, key);
                stmt2.executeUpdate();
        }
    }

}
