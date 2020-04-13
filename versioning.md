## NORMAL VERSION 
A normal version number MUST take the form X.Y.Z where X, Y, and Z are non-negative integers, and MUST NOT contain leading zeroes but for draft versions. X is the major version, Y is the minor version, and Z is the patch version. Each element MUST increase numerically. For instance: 1.9.0 -> 1.10.0 -> 1.11.0.

    Once a versioned data model has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version.

    Major version zero (0.y.z) is for initial data model draft.

    Version 1.0.0 defines the first public data model version. The way in which the version number is incremented after this release is dependent on this document.

## PATCH VERSION
    Patch version Z (x.y.Z | x > 0) MUST be incremented if only backwards compatible fixes are introduced. A fix is defined as an internal change that fixes incorrect behavior.
    Patch version can be approved by any Subject administrator
    
## MINOR VERSION
    Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backwards compatible functionality is introduced to the data model (i.e. a new non required property is added). It MUST be incremented if any property is added. It MAY include patch level changes. Patch version MUST be reset to 0 when minor version is incremented.
    If data model does NOT belong to the Cross sector domain, patch version can be approved by any Subject administrator but notified to domain administrator. If the data model belongs to the Cross Sector domain if can be approved by Subjwect administrator but notified to all afffected domain administrators.

## MAJOR VERSION
    Major version X (X.y.z | X > 0) MUST be incremented if any backwards incompatible changes are introduced to the data model. It MAY also include minor and patch level changes. Patch and minor version MUST be reset to 0 when major version is incremented.
    This versions has to be approved by the management because it could impact 
