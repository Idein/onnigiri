{
  description = "onnigiri";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }: (system:
    let pkgs = nixpkgs.legacyPackages.${system};
        py = pkgs.python38;
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          pkgs.protobuf

          py
          py.pkgs.python-language-server
          py.pkgs.jedi
          py.pkgs.poetry
        ];

        shellHook = ''
          export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}
        '';
      };
    }
  );
}
