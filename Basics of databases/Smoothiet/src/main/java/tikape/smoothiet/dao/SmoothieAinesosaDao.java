
package tikape.smoothiet.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import tikape.smoothiet.database.Database;
import tikape.smoothiet.domain.SmoothieAinesosa;


public class SmoothieAinesosaDao implements Dao<SmoothieAinesosa, Integer> {

    private Database database;

    public SmoothieAinesosaDao(Database database) {
        this.database = database;
    }
    
    @Override
    public SmoothieAinesosa etsiYksi(Integer key) throws SQLException {
        throw new UnsupportedOperationException("Toiminto ei ole vielä käytössä.");
    }

    @Override
    public List<SmoothieAinesosa> etsiKaikki() throws SQLException {
        throw new UnsupportedOperationException("Toiminto ei ole vielä käytössä.");
    }

    @Override
    public SmoothieAinesosa tallenna(SmoothieAinesosa object) throws SQLException {
        SmoothieAinesosa olemassaolevaVaihe = etsiOlemassaolevaVaihe(object.getLisaysjarjestys(), object.getAinesosaId(), object.getSmoothieId());

        if (olemassaolevaVaihe != null) {
            return olemassaolevaVaihe;
        }

        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("INSERT INTO SmoothieAinesosa (lisaysjarjestys, maara, ohje, ainesosa_id, smoothie_id) VALUES (?, ?, ?, ?, ?);");
            stmt.setInt(1, object.getLisaysjarjestys());
            stmt.setString(2, object.getMaara());
            stmt.setString(3, object.getOhje());
            stmt.setInt(4, object.getAinesosaId());
            stmt.setInt(5, object.getSmoothieId());
            stmt.executeUpdate();
        }

        return etsiOlemassaolevaVaihe(object.getLisaysjarjestys(), object.getAinesosaId(), object.getSmoothieId());
    }
    
    private SmoothieAinesosa etsiOlemassaolevaVaihe(Integer jarjestys, Integer ainesosa, Integer smoothie) throws SQLException {
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT Ainesosa.nimi, SmoothieAinesosa.* FROM Ainesosa, SmoothieAinesosa WHERE SmoothieAinesosa.ainesosa_id = Ainesosa.id AND lisaysjarjestys = ? AND ainesosa_id = ? AND smoothie_id = ?");
            stmt.setInt(1, jarjestys);
            stmt.setInt(2, ainesosa);
            stmt.setInt(3, smoothie);

            ResultSet result = stmt.executeQuery();
            if (!result.next()) {
                return null;
            }

            return new SmoothieAinesosa(result.getInt("id"), result.getInt("smoothie_id"), result.getInt("ainesosa_id"), result.getInt("lisaysjarjestys"), result.getString("nimi"), result.getString("maara"), result.getString("ohje"));
        }
    }

    @Override
    public void poista(Integer key) throws SQLException {
        try (Connection conn = database.getConnection()) {
                PreparedStatement stmt = conn.prepareStatement("DELETE FROM SmoothieAinesosa WHERE id = ?");
                stmt.setInt(1, key);
                stmt.executeUpdate();
        }
    }
    
    public List<SmoothieAinesosa> etsiSmoothienAinesosat(Integer key) throws SQLException {
        List<SmoothieAinesosa> sa = new ArrayList<>();
        
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT Ainesosa.nimi, SmoothieAinesosa.* FROM Ainesosa, SmoothieAinesosa WHERE SmoothieAinesosa.ainesosa_id = Ainesosa.id AND smoothie_id = ? ORDER BY lisaysjarjestys");
            stmt.setInt(1, key);
            ResultSet result = stmt.executeQuery();
            
            while (result.next()) {
                sa.add(new SmoothieAinesosa(result.getInt("id"), result.getInt("smoothie_id"), result.getInt("ainesosa_id"), result.getInt("lisaysjarjestys"), result.getString("nimi"), result.getString("maara"), result.getString("ohje")));
            }
        }
        return sa;
    }
    
    public List<Integer> etsiSmoothieIdAinesosalla(Integer key) throws SQLException {
        List<Integer> smoothieIdt = new ArrayList<>();
        
        try (Connection conn = database.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement("SELECT smoothie_id FROM SmoothieAinesosa WHERE SmoothieAinesosa.ainesosa_id = ? GROUP BY smoothie_id");
            stmt.setInt(1, key);
            ResultSet result = stmt.executeQuery();
            
            while (result.next()) {
                smoothieIdt.add(result.getInt("smoothie_id"));
            }
        }
        return smoothieIdt;
    }
    
    public void poistaSmoothiet(Integer key) throws SQLException {
        try (Connection conn = database.getConnection()) {
                PreparedStatement stmt = conn.prepareStatement("DELETE FROM SmoothieAinesosa WHERE smoothie_id = ?");
                stmt.setInt(1, key);
                stmt.executeUpdate();
        }
    }
    
        public void poistaAinesosat(Integer key) throws SQLException {
        try (Connection conn = database.getConnection()) {
                PreparedStatement stmt = conn.prepareStatement("DELETE FROM SmoothieAinesosa WHERE ainesosa_id = ?");
                stmt.setInt(1, key);
                stmt.executeUpdate();
        }
    }

}
