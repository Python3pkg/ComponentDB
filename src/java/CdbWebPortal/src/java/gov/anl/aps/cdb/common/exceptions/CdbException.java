/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.common.exceptions;

import gov.anl.aps.cdb.common.constants.CdbStatus;

/**
 * Generic CDB exception, used as base class for all CDB exceptions.
 */
public class CdbException extends Exception {

    /**
     * Exception keys.
     */
    public static final String SIGNATURE_KEY = "__cdb_exception__";
    public static final String TYPE_KEY = "type";
    public static final String CODE_KEY = "code";
    public static final String ARGS_KEY = "args";

    private String error = null;

    /**
     * Default constructor.
     */
    public CdbException() {
        super();
    }

    /**
     * Constructor using error message.
     *
     * @param message error message
     */
    public CdbException(String message) {
        super(message);
    }

    /**
     * Constructor using throwable object.
     *
     * @param throwable throwable object
     */
    public CdbException(Throwable throwable) {
        super(throwable);
    }

    /**
     * Constructor using error message and throwable object.
     *
     * @param message error message
     * @param throwable throwable object
     */
    public CdbException(String message, Throwable throwable) {
        super(message, throwable);
    }

    public int getErrorCode() {
        return CdbStatus.CDB_ERROR;
    }

    public void setErrorMessage(String error) {
        this.error = error;
    }

    public String getErrorMessage() {
        if (error != null) {
            return error;
        }
        return super.getMessage();
    }

    /**
     * Convert exception to string, overriding string output if error message is
     * set.
     *
     * @return exception string
     */
    @Override
    public String toString() {
        if (error != null) {
            return error;
        } else {
            return super.toString();
        }
    }
}
