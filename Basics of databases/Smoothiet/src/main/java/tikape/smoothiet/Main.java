package tikape.smoothiet;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import spark.ModelAndView;
import spark.Spark;
import spark.template.thymeleaf.ThymeleafTemplateEngine;
import tikape.smoothiet.database.Database;
import tikape.smoothiet.dao.*;
import tikape.smoothiet.domain.*;

public class Main {

    public static void main(String[] args) throws Exception {
        if (System.getenv(
                "PORT") != null) {
            Spark.port(Integer.valueOf(System.getenv("PORT")));
        }

        Database database = new Database("jdbc:sqlite:smoothiet.db");
        AinesosaDao ainesosat = new AinesosaDao(database);
        SmoothieDao smoothiet = new SmoothieDao(database);
        SmoothieAinesosaDao sa = new SmoothieAinesosaDao(database);

        Spark.get("/", (req, res) -> {
            HashMap map = new HashMap<>();

            map.put("smoothiet", smoothiet.etsiKaikki());

            return new ModelAndView(map, "index");
        }, new ThymeleafTemplateEngine());

        Spark.get("/ainesosasmoothiet/:id/", (req, res) -> {
            HashMap map = new HashMap<>();
            Integer ainesosaId = Integer.parseInt(req.params(":id"));

            List<Integer> smoothieIdLista = sa.etsiSmoothieIdAinesosalla(ainesosaId);
            List<Smoothie> smoothieLista = new ArrayList();
            Ainesosa a = ainesosat.etsiYksi(ainesosaId);
            int maara = 0;
            for (int i = 0; i < smoothieIdLista.size(); i++) {
                int id = smoothieIdLista.get(i);
                Smoothie seuraava = smoothiet.etsiYksi(id);
                smoothieLista.add(seuraava);
                maara++;
            }
            map.put("smoothiet", smoothieLista);
            map.put("ainesosa", a);
            map.put("maara", maara);
    
            return new ModelAndView(map, "ainesosasmoothiet");
        }, new ThymeleafTemplateEngine());

        Spark.get("/smoothieluonti/", (req, res) -> {
            HashMap map = new HashMap<>();

            map.put("smoothiet", smoothiet.etsiKaikki());
            map.put("ainesosat", ainesosat.etsiKaikki());

            return new ModelAndView(map, "smoothieluonti");
        }, new ThymeleafTemplateEngine());

        Spark.get("/ainesosa/", (req, res) -> {
            HashMap map = new HashMap<>();

            map.put("ainesosat", ainesosat.etsiKaikki());

            return new ModelAndView(map, "ainesosa");
        }, new ThymeleafTemplateEngine());

        Spark.get("/smoothie/:id/", (req, res) -> {
            HashMap map = new HashMap<>();

            Integer smoothieId = Integer.parseInt(req.params(":id"));

            map.put("sa", sa.etsiSmoothienAinesosat(smoothieId));
            map.put("smoothie", smoothiet.etsiYksi(smoothieId));

            return new ModelAndView(map, "smoothie");
        }, new ThymeleafTemplateEngine());

        Spark.post("/smoothienlisays", (req, res) -> {
            if (!syoteOk(req.queryParams("smoothie"))) {
                res.redirect("/smoothieluonti/");
                return "";
            }
            Smoothie smoothie = new Smoothie(-1, req.queryParams("smoothie"));
            smoothiet.tallenna(smoothie);
            res.redirect("/smoothieluonti/");
            return "";
        });

        Spark.post("/smoothieainesosanlisays", (req, res) -> {
            if (!syoteOk(req.queryParams("ohje")) || !syoteOk(req.queryParams("maara")) || !syoteOk(req.queryParams("jarjestys")) || !arvoPositiivinen(req.queryParams("jarjestys"))) {
                res.redirect("/smoothieluonti/");
                return "";
            }
            SmoothieAinesosa ainesosa = new SmoothieAinesosa(-1, Integer.parseInt(req.queryParams("smoothieId")), Integer.parseInt(req.queryParams("ainesosaId")), Integer.parseInt(req.queryParams("jarjestys")), "", req.queryParams("maara"), req.queryParams("ohje"));
            sa.tallenna(ainesosa);
            res.redirect("/smoothieluonti/");
            return "";
        });

        Spark.post("/smoothie/:id/delete", (req, res) -> {
            smoothiet.poista(Integer.parseInt(req.params(":id")));
            sa.poistaSmoothiet(Integer.parseInt(req.params(":id")));
            res.redirect("/smoothieluonti/");
            return "";
        });

        Spark.post("/ainesosanlisays", (req, res) -> {
            if (!syoteOk(req.queryParams("ainesosa"))) {
                res.redirect("/ainesosa/");
                return "";
            }
            Ainesosa ainesosa = new Ainesosa(-1, req.queryParams("ainesosa"), "");
            ainesosat.tallenna(ainesosa);
            res.redirect("/ainesosa/");
            return "";
        });

        Spark.post("/ainesosa/:id/delete", (req, res) -> {
            ainesosat.poista(Integer.parseInt(req.params(":id")));
            sa.poistaAinesosat(Integer.parseInt(req.params(":id")));
            res.redirect("/ainesosa/");
            return "";
        });
    }

    private static boolean syoteOk(String syote) {
        if (!syote.isEmpty()) {
            return true;
        }
        return false;
    }

    private static boolean arvoPositiivinen(String syote) {
        if (Integer.parseInt(syote) > 0) {
            return true;
        }
        return false;
    }
}
