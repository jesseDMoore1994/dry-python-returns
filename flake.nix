{
  description = "A flake storing the dependencies of the returns demo";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    returns-nix.url = "github:jesseDMoore1994/returns-nix";
    patat-nix.url = "github:jesseDMoore1994/patat-nix";
  };

  outputs = { self, nixpkgs, flake-utils, returns-nix, patat-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in rec {
        devShell = pkgs.mkShell {
            buildInputs = [
              patat-nix.defaultPackage.${system}
              pkgs.cabal-install
              (pkgs.ghc.withPackages (hs: [ hs.wreq ]))
              pkgs.ghcid
              pkgs.python3Packages.requests
              pkgs.zlib
              returns-nix.defaultPackage.${system}
            ];
        };
      }
    );
}
