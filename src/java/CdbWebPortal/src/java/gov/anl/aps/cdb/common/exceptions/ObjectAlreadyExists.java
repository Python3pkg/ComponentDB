/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.common.exceptions;

import gov.anl.aps.cdb.common.constants.CdbStatus;

/**
 * Object already exists exception.
 */
public class ObjectAlreadyExists extends CdbException {

    /**
     * Default constructor.
     */
    public ObjectAlreadyExists() {
        super();
    }

    /**
     * Constructor using error message.
     *
     * @param message error message
     */
    public ObjectAlreadyExists(String message) {
        super(message);
    }

    /**
     * Constructor using throwable object.
     *
     * @param throwable throwable object
     */
    public ObjectAlreadyExists(Throwable throwable) {
        super(throwable);
    }

    /**
     * Constructor using error message and throwable object.
     *
     * @param message error message
     * @param throwable throwable object
     */
    public ObjectAlreadyExists(String message, Throwable throwable) {
        super(message, throwable);
    }

    @Override
    public int getErrorCode() {
        return CdbStatus.CDB_OBJECT_ALREADY_EXISTS;
    }    
}
