/**
 * (C) Copyright 2016-2022 Intel Corporation.
 *
 * SPDX-License-Identifier: BSD-2-Clause-Patent
 */
/**
 * dc_cont, ds_cont: RPC Protocol Serialization Functions
 */
#define D_LOGFAC	DD_FAC(container)

#include <daos/rpc.h>
#include "rpc.h"

static int
crt_proc_struct_rsvc_hint(crt_proc_t proc, crt_proc_op_t proc_op,
			  struct rsvc_hint *hint)
{
	int rc;

	rc = crt_proc_uint32_t(proc, proc_op, &hint->sh_flags);
	if (rc != 0)
		return -DER_HG;

	rc = crt_proc_uint32_t(proc, proc_op, &hint->sh_rank);
	if (rc != 0)
		return -DER_HG;

	rc = crt_proc_uint64_t(proc, proc_op, &hint->sh_term);
	if (rc != 0)
		return -DER_HG;

	return 0;
}

static int
crt_proc_daos_epoch_range_t(crt_proc_t proc, crt_proc_op_t proc_op,
			    daos_epoch_range_t *erange)
{
	int rc;

	rc = crt_proc_uint64_t(proc, proc_op, &erange->epr_lo);
	if (rc != 0)
		return -DER_HG;

	rc = crt_proc_uint64_t(proc, proc_op, &erange->epr_hi);
	if (rc != 0)
		return -DER_HG;

	return 0;
}

CRT_RPC_DEFINE(cont_op, DAOS_ISEQ_CONT_OP, DAOS_OSEQ_CONT_OP)

static int
crt_proc_struct_cont_op_in(crt_proc_t proc, crt_proc_op_t proc_op,
			   struct cont_op_in *data)
{
	return crt_proc_cont_op_in(proc, data);
}

static int
crt_proc_struct_cont_op_out(crt_proc_t proc, crt_proc_op_t proc_op,
			    struct cont_op_out *data)
{
	return crt_proc_cont_op_out(proc, data);
}

CRT_RPC_DEFINE(cont_create, DAOS_ISEQ_CONT_CREATE, DAOS_OSEQ_CONT_CREATE)
CRT_RPC_DEFINE(cont_destroy, DAOS_ISEQ_CONT_DESTROY, DAOS_OSEQ_CONT_DESTROY)
CRT_RPC_DEFINE(cont_destroy_bylabel, DAOS_ISEQ_CONT_DESTROY_BYLABEL,
	       DAOS_OSEQ_CONT_DESTROY)
CRT_RPC_DEFINE(cont_open, DAOS_ISEQ_CONT_OPEN, DAOS_OSEQ_CONT_OPEN)
CRT_RPC_DEFINE(cont_open_v7, DAOS_ISEQ_CONT_OPEN, DAOS_OSEQ_CONT_OPEN_V7)
CRT_RPC_DEFINE(cont_open_v6, DAOS_ISEQ_CONT_OPEN, DAOS_OSEQ_CONT_OPEN_V6)
CRT_RPC_DEFINE(cont_open_bylabel, DAOS_ISEQ_CONT_OPEN_BYLABEL,
	       DAOS_OSEQ_CONT_OPEN_BYLABEL)
CRT_RPC_DEFINE(cont_open_bylabel_v7, DAOS_ISEQ_CONT_OPEN_BYLABEL,
	       DAOS_OSEQ_CONT_OPEN_BYLABEL_V7)
CRT_RPC_DEFINE(cont_open_bylabel_v6, DAOS_ISEQ_CONT_OPEN_BYLABEL,
	       DAOS_OSEQ_CONT_OPEN_BYLABEL_V6)
CRT_RPC_DEFINE(cont_close, DAOS_ISEQ_CONT_CLOSE, DAOS_OSEQ_CONT_CLOSE)
CRT_RPC_DEFINE(cont_query, DAOS_ISEQ_CONT_QUERY, DAOS_OSEQ_CONT_QUERY)
CRT_RPC_DEFINE(cont_query_v7, DAOS_ISEQ_CONT_QUERY, DAOS_OSEQ_CONT_QUERY_V7)
CRT_RPC_DEFINE(cont_query_v6, DAOS_ISEQ_CONT_QUERY, DAOS_OSEQ_CONT_QUERY_V6)
CRT_RPC_DEFINE(cont_oid_alloc, DAOS_ISEQ_CONT_OID_ALLOC,
		DAOS_OSEQ_CONT_OID_ALLOC)
CRT_RPC_DEFINE(cont_attr_list, DAOS_ISEQ_CONT_ATTR_LIST,
		DAOS_OSEQ_CONT_ATTR_LIST)
CRT_RPC_DEFINE(cont_attr_get, DAOS_ISEQ_CONT_ATTR_GET, DAOS_OSEQ_CONT_ATTR_GET)
CRT_RPC_DEFINE(cont_attr_set, DAOS_ISEQ_CONT_ATTR_SET, DAOS_OSEQ_CONT_ATTR_SET)
CRT_RPC_DEFINE(cont_attr_del, DAOS_ISEQ_CONT_ATTR_DEL, DAOS_OSEQ_CONT_ATTR_DEL)
CRT_RPC_DEFINE(cont_epoch_op, DAOS_ISEQ_CONT_EPOCH_OP, DAOS_OSEQ_CONT_EPOCH_OP)
CRT_RPC_DEFINE(cont_snap_list, DAOS_ISEQ_CONT_SNAP_LIST,
		DAOS_OSEQ_CONT_SNAP_LIST)
CRT_RPC_DEFINE(cont_snap_create, DAOS_ISEQ_CONT_EPOCH_OP,
		DAOS_OSEQ_CONT_EPOCH_OP)
CRT_RPC_DEFINE(cont_snap_destroy, DAOS_ISEQ_CONT_EPOCH_OP,
		DAOS_OSEQ_CONT_EPOCH_OP)
CRT_RPC_DEFINE(cont_tgt_destroy, DAOS_ISEQ_TGT_DESTROY, DAOS_OSEQ_TGT_DESTROY)
CRT_RPC_DEFINE(cont_tgt_query, DAOS_ISEQ_TGT_QUERY, DAOS_OSEQ_TGT_QUERY)
CRT_RPC_DEFINE(cont_tgt_epoch_aggregate, DAOS_ISEQ_CONT_TGT_EPOCH_AGGREGATE,
		DAOS_OSEQ_CONT_TGT_EPOCH_AGGREGATE)
CRT_RPC_DEFINE(cont_tgt_snapshot_notify, DAOS_ISEQ_CONT_TGT_SNAPSHOT_NOTIFY,
		DAOS_OSEQ_CONT_TGT_SNAPSHOT_NOTIFY)
CRT_RPC_DEFINE(cont_prop_set, DAOS_ISEQ_CONT_PROP_SET, DAOS_OSEQ_CONT_PROP_SET)
CRT_RPC_DEFINE(cont_acl_update, DAOS_ISEQ_CONT_ACL_UPDATE,
	       DAOS_OSEQ_CONT_ACL_UPDATE)
CRT_RPC_DEFINE(cont_acl_delete, DAOS_ISEQ_CONT_ACL_DELETE,
	       DAOS_OSEQ_CONT_ACL_DELETE)

/* Define for cont_rpcs[] array population below.
 * See CONT_PROTO_*_RPC_LIST macro definition
 */
#define X(a, b, c, d, e)	\
{				\
	.prf_flags   = b,	\
	.prf_req_fmt = c,	\
	.prf_hdlr    = NULL,	\
	.prf_co_ops  = NULL,	\
}

static struct crt_proto_rpc_format cont_proto_rpc_fmt_v7[] = {
	CONT_PROTO_CLI_RPC_LIST(7, ds_cont_op_handler_v7),
	CONT_PROTO_SRV_RPC_LIST,
};

static struct crt_proto_rpc_format cont_proto_rpc_fmt_v6[] = {
	CONT_PROTO_CLI_RPC_LIST(6, ds_cont_op_handler_v6),
	CONT_PROTO_SRV_RPC_LIST,
};

#undef X

struct crt_proto_format cont_proto_fmt_v7 = {
	.cpf_name  = "cont",
	.cpf_ver   = 7,
	.cpf_count = ARRAY_SIZE(cont_proto_rpc_fmt_v7),
	.cpf_prf   = cont_proto_rpc_fmt_v7,
	.cpf_base  = DAOS_RPC_OPCODE(0, DAOS_CONT_MODULE, 0)
};

struct crt_proto_format cont_proto_fmt_v6 = {
	.cpf_name  = "cont",
	.cpf_ver   = 6,
	.cpf_count = ARRAY_SIZE(cont_proto_rpc_fmt_v6),
	.cpf_prf   = cont_proto_rpc_fmt_v6,
	.cpf_base  = DAOS_RPC_OPCODE(0, DAOS_CONT_MODULE, 0)
};
