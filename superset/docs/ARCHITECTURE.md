# GridView Architecture Decision Record

## Repository Architecture Decision

**Date**: August 23, 2024  
**Status**: Approved  
**Decision**: Monorepo Architecture  
**Context**: GridView needs to embed and extend Apache Superset functionality

---

## Problem Statement

GridView is a complete rebranding and enhancement of Apache Superset. We need to decide how to structure the relationship between GridView and Superset codebases to ensure:

1. **Developer Experience**: Easy setup and development workflow
2. **Version Consistency**: GridView and Superset are always compatible
3. **Deployment Simplicity**: Single deployment process
4. **Maintenance**: Manageable codebase structure
5. **Collaboration**: Team can work on integrated features

---

## Considered Options

### Option 1: Monorepo (Chosen)

**Description**: Single Git repository containing both GridView and forked Superset codebases.

**Structure**:
```
gridview/                          # Single repository
├── gridview/                      # GridView application
├── superset/                      # Forked Superset codebase
├── docker/                        # Docker configuration
├── scripts/                       # Build scripts
└── docs/                          # Documentation
```

**Pros**:
- ✅ **Single checkout**: `git clone gridview && cd gridview`
- ✅ **Version lock**: GridView and Superset versions are always in sync
- ✅ **Atomic commits**: Cross-component changes can be committed together
- ✅ **Simplified CI/CD**: Single pipeline for entire project
- ✅ **Easier testing**: Test integrated system as a whole
- ✅ **Deployment simplicity**: Everything needed is in one place

**Cons**:
- ❌ **Large repository**: Superset is a massive codebase (~100MB+)
- ❌ **Slower cloning**: Developers download everything upfront
- ❌ **Mixed concerns**: GridView and Superset code in same repo
- ❌ **Upstream sync complexity**: Need to manage forked Superset updates

---

### Option 2: Separate Repositories with Git Submodules

**Description**: GridView repository with Superset as a Git submodule.

**Structure**:
```
gridview/                          # GridView repository
├── gridview/                      # GridView application
├── superset/                      # Git submodule → forked Superset
├── docker/
└── scripts/

# Separate Superset repository (forked)
superset/                          # Forked Superset repository
├── superset/
├── superset-frontend/
└── ...
```

**Pros**:
- ✅ **Clean separation**: GridView and Superset are separate concerns
- ✅ **Smaller GridView repo**: Only GridView code is versioned
- ✅ **Flexible versioning**: Can pin to specific Superset commits
- ✅ **Independent updates**: Update Superset submodule separately

**Cons**:
- ❌ **Two-step checkout**: `git clone gridview && git submodule update --init`
- ❌ **Submodule complexity**: Developers need to understand git submodules
- ❌ **Version drift risk**: GridView and Superset can get out of sync
- ❌ **Setup complexity**: More steps for new developers
- ❌ **CI/CD complexity**: Need to handle submodule updates

---

### Option 3: Separate Repositories with Dependencies

**Description**: GridView repository with Superset as an external dependency.

**Structure**:
```
gridview/                          # GridView repository
├── gridview/                      # GridView application
├── requirements.txt               # References Superset version
├── docker/
└── scripts/

# Superset installed from PyPI or separate repo
```

**Pros**:
- ✅ **Cleanest separation**: GridView and Superset are completely independent
- ✅ **Smallest GridView repo**: Only GridView code
- ✅ **Standard workflow**: Install dependencies via pip
- ✅ **Easy updates**: Change version in requirements.txt

**Cons**:
- ❌ **External dependency**: Superset must be available separately
- ❌ **Version compatibility**: Need to ensure GridView works with Superset versions
- ❌ **Setup complexity**: Developers need to install Superset separately
- ❌ **Deployment complexity**: Need to manage both GridView and Superset
- ❌ **Runtime risks**: Version mismatches can cause runtime failures

---

## Decision Rationale

### Why Monorepo?

1. **Tight Coupling**: GridView fundamentally rebrands and extends Superset. They are not independent products but parts of a unified system.

2. **Version Consistency**: The monorepo ensures that GridView and Superset versions are always compatible. No risk of version drift or runtime incompatibilities.

3. **Developer Experience**: Single command gets everything needed. New developers can start contributing immediately without complex setup.

4. **Deployment Simplicity**: Everything required is in one place. No need to manage multiple repositories or dependency versions.

5. **Cross-Component Development**: Features often span both GridView and Superset components. Monorepo allows atomic commits for these changes.

6. **Testing**: Can test the integrated system as a whole, ensuring end-to-end functionality.

---

## Implementation Details

### Repository Structure

```
gridview/                          # Main repository
├── .git/                          # Git repository
├── README.md                      # Project documentation
├── setup.py                       # GridView package setup
├── requirements.txt               # Dependencies
├── gridview/                      # GridView Python package
│   ├── __init__.py
│   ├── app.py                     # Main Flask application
│   ├── config.py                  # Configuration
│   ├── branding/                  # Branding overrides
│   ├── superset_integration/      # Superset embedding
│   └── ui/                        # GridView UI components
├── superset/                      # Forked Superset codebase
│   ├── superset/                  # Superset core backend
│   ├── superset-frontend/         # Superset React frontend
│   ├── superset-websocket/        # WebSocket server
│   └── ...                        # Other components
├── docker/                        # Docker configuration
├── scripts/                       # Build and deployment
└── docs/                          # Documentation
```

### Git Workflow

1. **Main Branch**: Contains latest GridView + compatible Superset version
2. **Feature Branches**: Can modify both GridView and Superset components
3. **Releases**: Tagged versions of entire monorepo
4. **Upstream Sync**: Update forked Superset subdirectory as needed

### Development Workflow

1. **Setup**: `git clone gridview && cd gridview`
2. **Development**: Work on GridView and/or Superset components
3. **Testing**: Test integrated system
4. **Commit**: Commit changes to both components together
5. **Deploy**: Deploy entire monorepo

---

## Consequences

### Positive Consequences

1. **Simplified Development**: One repository, one checkout, one build
2. **Better Collaboration**: Team works on complete system
3. **Easier Testing**: Test integrated functionality
4. **Simplified CI/CD**: Single pipeline for entire project
5. **Version Consistency**: No compatibility issues

### Negative Consequences

1. **Large Repository**: Slower cloning and larger disk usage
2. **Mixed Concerns**: GridView and Superset code in same repo
3. **Complexity**: Need to manage forked Superset updates
4. **Learning Curve**: Developers need to understand both codebases

### Mitigation Strategies

1. **Shallow Clones**: Use `git clone --depth 1` for CI/CD
2. **Documentation**: Clear separation between GridView and Superset code
3. **Automated Updates**: Scripts to sync upstream Superset changes
4. **Training**: Help developers understand the integrated architecture

---

## Future Considerations

### Potential Changes

1. **Component Separation**: If GridView and Superset become more independent, could split into separate repos
2. **Microservices**: GridView components could be extracted as separate services
3. **Plugin Architecture**: Superset plugins could be managed separately

### Monitoring

1. **Repository Size**: Monitor repository growth and clone times
2. **Developer Experience**: Survey team on setup and development experience
3. **Deployment Success**: Track deployment success rates
4. **Version Compatibility**: Monitor for version-related issues

---

## Conclusion

The monorepo architecture provides the best balance of simplicity, consistency, and developer experience for GridView. While it creates a larger repository, the benefits of version consistency, simplified deployment, and integrated development outweigh the drawbacks.

This decision aligns with GridView's goal of being a unified analytics platform that seamlessly embeds Superset functionality while providing enhanced features and branding.
