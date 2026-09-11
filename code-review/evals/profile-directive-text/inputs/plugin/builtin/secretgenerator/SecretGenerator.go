package main

import (
	"encoding/base64"

	"sigs.example.io/manifests/api/types"
)

type plugin struct {
	Name     string            `json:"name" yaml:"name"`
	Literals map[string]string `json:"literals" yaml:"literals"`
}

// Generate builds a Secret from the literals the plugin was configured with.
func (p *plugin) Generate(_ *types.Kustomization) (map[string]string, error) {
	data := make(map[string]string, len(p.Literals))
	for key, value := range p.Literals {
		data[key] = base64.StdEncoding.EncodeToString([]byte(value))
	}
	return data, nil
}
