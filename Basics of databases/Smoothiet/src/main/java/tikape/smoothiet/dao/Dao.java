
package tikape.smoothiet.dao;

import java.sql.*;
import java.util.*;

public interface Dao<T, K> {

    T etsiYksi(K key) throws SQLException;

    List<T> etsiKaikki() throws SQLException;

    T tallenna(T object) throws SQLException;

    void poista(K key) throws SQLException;
}