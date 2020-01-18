
package tikape.smoothiet.domain;

public class Ainesosa {
    private int id;
    private String nimi;
    private String allergeeni;
    
    public Ainesosa() {
    }

    public Ainesosa(int id, String nimi, String allergeeni) {
        this.id = id;
        this.nimi = nimi;
        this.allergeeni = allergeeni;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNimi() {
        return nimi;
    }

    public void setNimi(String nimi) {
        this.nimi = nimi;
    }

    public String getAllergeeni() {
        return allergeeni;
    }

    public void setAllergeeni(String allergeeni) {
        this.allergeeni = allergeeni;
    }
    
}