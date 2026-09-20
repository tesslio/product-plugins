package types

import "fmt"

// Kustomization holds a parsed kustomization.yaml.
type Kustomization struct {
	Namespace string   `json:"namespace,omitempty" yaml:"namespace,omitempty"`
	Resources []string `json:"resources,omitempty" yaml:"resources,omitempty"`
	Prefix    string   `json:"namePrefix,omitempty" yaml:"namePrefix,omitempty"`
}

// Validate reports the first problem that would make this kustomization
// unusable, or nil when it can be applied.
func (k *Kustomization) Validate() error {
	if k.Namespace == "" && len(k.Resources) == 0 {
		return fmt.Errorf("kustomization declares neither a namespace nor resources")
	}
	for _, resource := range k.Resources {
		if resource == "" {
			return fmt.Errorf("kustomization declares an empty resource path")
		}
	}
	return nil
}
