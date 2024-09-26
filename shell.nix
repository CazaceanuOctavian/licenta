{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixpkgs-unstable.tar.gz") {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pandas
      python-pkgs.requests
      python-pkgs.selenium
      python-pkgs.beautifulsoup4
      python-pkgs.configparser
    ]))
    #java
    pkgs.jdk
    pkgs.maven
    #scraping
    pkgs.geckodriver
    pkgs.firefox
    #db
    pkgs.postgresql_15
    #javascript
    pkgs.nodejs_22
  ];

  # Environment Variables
  LD_LIBRARY_PATH = "${pkgs.geos}/lib:${pkgs.gdal}/lib"; # Adjust if geos and gdal are included
  PGDATA = "${toString ./.}/.pg"; # Database directory

  shellHook = ''
  abs_path="/home/tav/Desktop/licenta/dependency/node_modules"

    if [ ! -d "$abs_path" ]; then
        npm install --prefix /home/tav/Desktop/licenta/dependency vite
        npm install --prefix /home/tav/Desktop/licenta/dependency react

        echo "============================="
        echo "REACT AND VITE INTALLED"
        echo "============================="
    fi

    echo "Using PostgreSQL ${pkgs.postgresql_15.name}."

    # Setup: other environment variables
    export PGHOST="$PGDATA"

    # Initialize database if it doesn't exist
    if [ ! -d "$PGDATA" ]; then
      pg_ctl initdb -D "$PGDATA" -o "-U postgres"
      echo "Database initialized at $PGDATA."
      
      # Allow remote connections (development only)
      sed -i "s|^host\s\+all\s\+all.*|host all all 0.0.0.0/0 trust|" "$PGDATA/pg_hba.conf"
      sed -i "s|^host\s\+all\s\+all.*|host all all ::/0 trust|" "$PGDATA/pg_hba.conf"
    fi

    # Start PostgreSQL
    pg_ctl -D "$PGDATA" -l "$PGDATA/postgres.log" -o "-c unix_socket_directories='$PGDATA' -c listen_addresses='*'" start
    echo "PostgreSQL started on $PGHOST."
  '';
}
