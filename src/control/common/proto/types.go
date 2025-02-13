//
// (C) Copyright 2019-2022 Intel Corporation.
//
// SPDX-License-Identifier: BSD-2-Clause-Patent
//

package proto

import (
	"fmt"
	"strings"

	"github.com/daos-stack/daos/src/control/common"
	"github.com/daos-stack/daos/src/control/common/proto/convert"
	ctlpb "github.com/daos-stack/daos/src/control/common/proto/ctl"
	mgmtpb "github.com/daos-stack/daos/src/control/common/proto/mgmt"
	"github.com/daos-stack/daos/src/control/server/storage"
)

// NvmeHealth is an alias for protobuf BioHealthResp message.
type NvmeHealth ctlpb.BioHealthResp

// FromNative converts storage package type to protobuf equivalent.
func (pb *NvmeHealth) FromNative(native *storage.NvmeHealth) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *NvmeHealth) ToNative() (*storage.NvmeHealth, error) {
	native := new(storage.NvmeHealth)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *NvmeHealth) AsProto() *ctlpb.BioHealthResp {
	return (*ctlpb.BioHealthResp)(pb)
}

// NvmeNamespace is an alias for protobuf NvmeController_Namespace message.
type NvmeNamespace ctlpb.NvmeController_Namespace

// FromNative converts storage package type to protobuf equivalent.
func (pb *NvmeNamespace) FromNative(native *storage.NvmeNamespace) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *NvmeNamespace) ToNative() (*storage.NvmeNamespace, error) {
	native := new(storage.NvmeNamespace)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *NvmeNamespace) AsProto() *ctlpb.NvmeController_Namespace {
	return (*ctlpb.NvmeController_Namespace)(pb)
}

// NvmeNamespaces is an alias for protobuf NvmeController_Namespace message slice
// representing namespaces existing on a NVMe SSD.
type NvmeNamespaces []*ctlpb.NvmeController_Namespace

// SmdDevice is an alias for protobuf SmdDevice message
// representing DAOS server meta data existing on a NVMe SSD.
type SmdDevice ctlpb.SmdDevice

// FromNative converts storage package type to protobuf equivalent.
func (pb *SmdDevice) FromNative(native *storage.SmdDevice) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *SmdDevice) ToNative() (*storage.SmdDevice, error) {
	native := new(storage.SmdDevice)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *SmdDevice) AsProto() *ctlpb.SmdDevice {
	return (*ctlpb.SmdDevice)(pb)
}

// SmdDevices is an alias for protobuf SmdDevice message slice
// representing DAOS server meta data existing on a NVMe SSD.
type SmdDevices []*ctlpb.SmdDevice

// NvmeController is an alias for protobuf NvmeController message slice.
type NvmeController ctlpb.NvmeController

// FromNative converts storage package type to protobuf equivalent.
func (pb *NvmeController) FromNative(native *storage.NvmeController) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *NvmeController) ToNative() (*storage.NvmeController, error) {
	native := new(storage.NvmeController)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *NvmeController) AsProto() *ctlpb.NvmeController {
	return (*ctlpb.NvmeController)(pb)
}

// NvmeControllers is an alias for protobuf NvmeController message slice
// representing a number of NVMe SSD controllers installed on a storage node.
type NvmeControllers []*ctlpb.NvmeController

// FromNative converts storage package type to protobuf equivalent.
func (pb *NvmeControllers) FromNative(native storage.NvmeControllers) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *NvmeControllers) ToNative() (storage.NvmeControllers, error) {
	native := make(storage.NvmeControllers, 0, len(*pb))
	return native, convert.Types(pb, &native)
}

// NvmeControllerResults is an alias for protobuf NvmeControllerResult messages
// representing operation results on a number of NVMe controllers.
type NvmeControllerResults []*ctlpb.NvmeControllerResult

// HasErrors indicates whether any controller result has non-successful status.
func (ncr NvmeControllerResults) HasErrors() bool {
	for _, res := range ncr {
		if res.GetState().GetStatus() != ctlpb.ResponseStatus_CTL_SUCCESS {
			return true
		}
	}
	return false
}

// Errors reports summary string of errored results.
func (ncr NvmeControllerResults) Errors() string {
	var errs []string
	for _, res := range ncr {
		if res.GetState().GetStatus() != ctlpb.ResponseStatus_CTL_SUCCESS {
			errs = append(errs, fmt.Sprintf("%s: %s", res.GetPciAddr(),
				res.GetState().GetError()))
		}
	}
	return strings.Join(errs, ", ")
}

// ScmModule is an alias for protobuf ScmModule message representing an SCM
// persistent memory module installed on a storage node.
type ScmModule ctlpb.ScmModule

// FromNative converts storage package type to protobuf equivalent.
func (pb *ScmModule) FromNative(native *storage.ScmModule) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *ScmModule) ToNative() (*storage.ScmModule, error) {
	native := new(storage.ScmModule)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *ScmModule) AsProto() *ctlpb.ScmModule {
	return (*ctlpb.ScmModule)(pb)
}

// ScmModules is an alias for protobuf ScmModule message slice representing
// a number of SCM modules installed on a storage node.
type ScmModules []*ctlpb.ScmModule

// FromNative converts storage package type to protobuf equivalent.
func (pb *ScmModules) FromNative(native storage.ScmModules) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *ScmModules) ToNative() (storage.ScmModules, error) {
	native := make(storage.ScmModules, 0, len(*pb))
	return native, convert.Types(pb, &native)
}

// ScmModuleResults is an alias for protobuf ScmModuleResult message slice
// representing operation results on a number of SCM modules.
type ScmModuleResults []*ctlpb.ScmModuleResult

// ScmNamespace is an alias for protobuf ScmNamespace message representing a
// pmem block device created on an appdirect set of persistent memory modules.
type ScmNamespace ctlpb.ScmNamespace

// FromNative converts storage package type to protobuf equivalent.
func (pb *ScmNamespace) FromNative(native *storage.ScmNamespace) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *ScmNamespace) ToNative() (*storage.ScmNamespace, error) {
	native := new(storage.ScmNamespace)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *ScmNamespace) AsProto() *ctlpb.ScmNamespace {
	return (*ctlpb.ScmNamespace)(pb)
}

// ScmNamespaces is an alias for protobuf ScmNamespace message slice representing
// a number of SCM modules installed on a storage node.
type ScmNamespaces []*ctlpb.ScmNamespace

// FromNative converts storage package type to protobuf equivalent.
func (pb *ScmNamespaces) FromNative(native storage.ScmNamespaces) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *ScmNamespaces) ToNative() (storage.ScmNamespaces, error) {
	native := make(storage.ScmNamespaces, 0, len(*pb))
	return native, convert.Types(pb, &native)
}

// ScmMountPoint is an alias for protobuf ScmNamespace_Mount message representing
// the OS mount point target at which a pmem block device is mounted.
type ScmMountPoint ctlpb.ScmNamespace_Mount

// FromNative converts storage package type to protobuf equivalent.
func (pb *ScmMountPoint) FromNative(native *storage.ScmMountPoint) error {
	return convert.Types(native, pb)
}

// ToNative converts pointer receiver alias type to storage package equivalent.
func (pb *ScmMountPoint) ToNative() (*storage.ScmMountPoint, error) {
	native := new(storage.ScmMountPoint)
	return native, convert.Types(pb, native)
}

// AsProto converts pointer receiver alias type to protobuf type.
func (pb *ScmMountPoint) AsProto() *ctlpb.ScmNamespace_Mount {
	return (*ctlpb.ScmNamespace_Mount)(pb)
}

// ScmMountResults is an alias for protobuf ScmMountResult message slice
// representing operation results on a number of SCM mounts.
type ScmMountResults []*ctlpb.ScmMountResult

// HasErrors indicates whether any mount result has non-successful status.
func (smr ScmMountResults) HasErrors() bool {
	for _, res := range smr {
		if res.State.Status != ctlpb.ResponseStatus_CTL_SUCCESS {
			return true
		}
	}
	return false
}

// AccessControlListFromPB converts from the protobuf ACLResp structure to an
// AccessControlList structure.
func AccessControlListFromPB(pbACL *mgmtpb.ACLResp) *common.AccessControlList {
	if pbACL == nil {
		return &common.AccessControlList{}
	}
	return &common.AccessControlList{
		Entries:    pbACL.ACL,
		Owner:      pbACL.OwnerUser,
		OwnerGroup: pbACL.OwnerGroup,
	}
}
