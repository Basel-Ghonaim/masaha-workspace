import re
def edit(p, old, new, count=1):
    s=open(p,encoding='utf8').read()
    assert s.count(old)>=1, (p, old[:60])
    s=s.replace(old,new,count)
    open(p,'w',encoding='utf8',newline='').write(s)

edit('packages/shared/src/core/envelope.ts', """    errors?: FieldErrors;
    /** The X-Request-Id of this answer. */""", """    errors?: FieldErrors;
    /** The record a refusal is about, when it names one (api-contract §2). */
    details?: ErrorDetails;
    /** The X-Request-Id of this answer. */""")
edit('packages/shared/src/core/envelope.ts', """/** An error answer. */""", """/**
 * The record a refusal names, so the client can act on it without a second search. Today only
 * `ALREADY_OWNER` carries it: the owner's account, to link instead.
 */
export interface ErrorDetails {
  userId: number;
}

/** An error answer. */""")

p='apps/api/src/shared/errors/appError.ts'
edit(p, """import {
  ERROR_STATUSES,
  type DomainErrorCode,
  type ErrorType,
  type FieldErrors,
} from '@masaha/shared/core';""", """import {
  ERROR_STATUSES,
  type DomainErrorCode,
  type ErrorDetails,
  type ErrorType,
  type FieldErrors,
} from '@masaha/shared/core';""")
edit(p, """  readonly errors: FieldErrors | undefined;
  /** Set on""", """  readonly errors: FieldErrors | undefined;
  /** The record the refusal names (api-contract §2), when it names one. */
  readonly details: ErrorDetails | undefined;
  /** Set on""")
edit(p, """  constructor(type: ErrorType, code?: DomainErrorCode, message?: string, errors?: FieldErrors) {
    super(message ?? ERROR_MESSAGES[type]);
    this.type = type;
    this.status = ERROR_STATUSES[type];
    this.code = code;
    this.errors = errors;
  }""", """  constructor(
    type: ErrorType,
    code?: DomainErrorCode,
    message?: string,
    errors?: FieldErrors,
    details?: ErrorDetails,
  ) {
    super(message ?? ERROR_MESSAGES[type]);
    this.type = type;
    this.status = ERROR_STATUSES[type];
    this.code = code;
    this.errors = errors;
    this.details = details;
  }""")
edit(p, """  static conflict(code?: DomainErrorCode, message?: string, errors?: FieldErrors) {
    return new AppError('conflict', code, message, errors);
  }""", """  static conflict(
    code?: DomainErrorCode,
    message?: string,
    errors?: FieldErrors,
    details?: ErrorDetails,
  ) {
    return new AppError('conflict', code, message, errors, details);
  }""")
edit('apps/api/src/shared/errors/errorHandler.ts', """      ...(appError.errors && { errors: appError.errors }),
""", """      ...(appError.errors && { errors: appError.errors }),
      ...(appError.details && { details: appError.details }),
""")

p='apps/web/src/shared/errors/AppError.ts'
edit(p, "import type { DomainErrorCode, FieldErrors } from '@masaha/shared/core';", "import type { DomainErrorCode, ErrorDetails, FieldErrors } from '@masaha/shared/core';")
edit(p, """  errors?: FieldErrors | undefined;
  requestId?: string | undefined;""", """  errors?: FieldErrors | undefined;
  details?: ErrorDetails | undefined;
  requestId?: string | undefined;""")
edit(p, """  readonly errors: FieldErrors | undefined;
  /** The server's id""", """  readonly errors: FieldErrors | undefined;
  /** The record the refusal names (api-contract §2), such as the owner `ALREADY_OWNER` is about. */
  readonly details: ErrorDetails | undefined;
  /** The server's id""")
edit(p, """    this.errors = fields.errors;
""", """    this.errors = fields.errors;
    this.details = fields.details;
""")
p='apps/web/src/shared/errors/toAppError.ts'
edit(p, """  type DomainErrorCode,
  type ErrorEnvelope,""", """  type DomainErrorCode,
  type ErrorDetails,
  type ErrorEnvelope,""")
edit(p, """    errors: knownFieldErrors(envelope.errors),
""", """    errors: knownFieldErrors(envelope.errors),
    details: detailsOf(envelope.details),
""")
edit(p, """/** A response header, whatever""", """/** The record a refusal names, kept only in the shape the contract gives it. */
function detailsOf(value: unknown): ErrorDetails | undefined {
  if (typeof value !== 'object' || value === null || !('userId' in value)) return undefined;
  const { userId } = value;
  return typeof userId === 'number' && Number.isInteger(userId) && userId > 0
    ? { userId }
    : undefined;
}

/** A response header, whatever""")
edit('docs/api/api-contract.md', """    errors?: Record<string, string[]>,  // field → error codes, e.g. { "phone": ["invalid_format"] }
""", """    errors?: Record<string, string[]>,  // field → error codes, e.g. { "phone": ["invalid_format"] }
    details?: { userId: number },       // the record a refusal names, to act on it (only ALREADY_OWNER
                                        // today, §5 Owners (the admin); 2026-10-29, #PRNUM)
""")
