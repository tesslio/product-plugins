package loader

import (
	"os"
	"path/filepath"

	"sigs.example.io/manifests/api/types"
	"gopkg.in/yaml.v3"
)

// Load reads the kustomization at root and returns it parsed and validated.
func Load(root string) (*types.Kustomization, error) {
	raw, err := os.ReadFile(filepath.Join(root, "kustomization.yaml"))
	if err != nil {
		return nil, err
	}
	var k types.Kustomization
	if err := yaml.Unmarshal(raw, &k); err != nil {
		return nil, err
	}
	if err := k.Validate(); err != nil {
		return nil, err
	}
	return &k, nil
}

// LoadAll reads every kustomization under roots, in the order given.
func LoadAll(roots []string) ([]*types.Kustomization, error) {
	out := make([]*types.Kustomization, 0, len(roots))
	for _, root := range roots {
		k, err := Load(root)
		if err != nil {
			return nil, err
		}
		out = append(out, k)
	}
	return out, nil
}
