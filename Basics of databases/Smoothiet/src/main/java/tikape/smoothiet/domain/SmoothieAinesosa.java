
package tikape.smoothiet.domain;


public class SmoothieAinesosa {
    private int id;
    private int smoothieId;
    private int ainesosaId;
    private int lisaysjarjestys;
    private String ainesosanNimi;
    private String maara;
    private String ohje;
    
    public SmoothieAinesosa() {
    }

    public SmoothieAinesosa(int id, int smoothieId, int ainesosaId, int lisaysjarjestys, String ainesosanNimi, String maara, String ohje) {
        this.id = id;
        this.smoothieId = smoothieId;
        this.ainesosaId = ainesosaId;
        this.lisaysjarjestys = lisaysjarjestys;
        this.ainesosanNimi = ainesosanNimi;
        this.maara = maara;
        this.ohje = ohje;
    }

    public String getAinesosanNimi() {
        return ainesosanNimi;
    }

    public void setAinesosanNimi(String ainesosanNimi) {
        this.ainesosanNimi = ainesosanNimi;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getSmoothieId() {
        return smoothieId;
    }

    public void setSmoothieId(int smoothieId) {
        this.smoothieId = smoothieId;
    }

    public int getAinesosaId() {
        return ainesosaId;
    }

    public void setAinesosaId(int ainesosaId) {
        this.ainesosaId = ainesosaId;
    }

    public int getLisaysjarjestys() {
        return lisaysjarjestys;
    }

    public void setLisaysjarjestys(int lisaysjarjestys) {
        this.lisaysjarjestys = lisaysjarjestys;
    }

    public String getMaara() {
        return maara;
    }

    public void setMaara(String maara) {
        this.maara = maara;
    }

    public String getOhje() {
        return ohje;
    }

    public void setOhje(String ohje) {
        this.ohje = ohje;
    }
}
