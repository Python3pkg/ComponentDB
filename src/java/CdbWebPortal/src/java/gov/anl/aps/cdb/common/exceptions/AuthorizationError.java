/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.common.exceptions;

import gov.anl.aps.cdb.common.constants.CdbStatus;

/**
 * Authorization error exception.
 */
public class AuthorizationError extends CdbException {

    /**
     * Default constructor.
     */
    public AuthorizationError() {
        super();
    }

    /**
     * Constructor using error message.
     *
     * @param message error message
     */
    public AuthorizationError(String message) {
        super(message);
    }

    /**
     * Constructor using throwable object.
     *
     * @param throwable throwable object
     */
    public AuthorizationError(Throwable throwable) {
        super(throwable);
    }

    /**
     * Constructor using error message and throwable object.
     *
     * @param message error message
     * @param throwable throwable object
     */
    public AuthorizationError(String message, Throwable throwable) {
        super(message, throwable);
    }

    @Override
    public int getErrorCode() {
        return CdbStatus.CDB_AUTHORIZATION_ERROR;
    }      
}
