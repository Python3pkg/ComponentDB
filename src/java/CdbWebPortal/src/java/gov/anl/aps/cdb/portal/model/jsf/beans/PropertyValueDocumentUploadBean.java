/*
 * Copyright (c) UChicago Argonne, LLC. All rights reserved.
 * See LICENSE file.
 */
package gov.anl.aps.cdb.portal.model.jsf.beans;

import gov.anl.aps.cdb.portal.model.db.entities.PropertyValue;
import gov.anl.aps.cdb.common.utilities.FileUtility;
import gov.anl.aps.cdb.portal.utilities.GalleryUtility;
import gov.anl.aps.cdb.portal.utilities.SessionUtility;
import gov.anl.aps.cdb.portal.utilities.StorageUtility;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import javax.enterprise.context.SessionScoped;
import javax.inject.Named;
import org.apache.log4j.Logger;
import org.primefaces.event.FileUploadEvent;

import org.primefaces.model.UploadedFile;

/**
 * JSF bean for property value document upload.
 */
@Named("propertyValueDocumentUploadBean")
@SessionScoped
public class PropertyValueDocumentUploadBean implements Serializable{

    private static final Logger logger = Logger.getLogger(PropertyValueDocumentUploadBean.class.getName());

    private UploadedFile uploadedFile;
    private PropertyValue propertyValue;

    public UploadedFile getUploadedFile() {
        return uploadedFile;
    }

    public void setUploadedFile(UploadedFile uploadedFile) {
        this.uploadedFile = uploadedFile;
    }

    public PropertyValue getPropertyValue() {
        return propertyValue;
    }

    public void setPropertyValue(PropertyValue propertyValue) {
        this.propertyValue = propertyValue;
    }

    public void upload(PropertyValue propertyValue) {
        this.propertyValue = propertyValue;
        Path uploadDirPath;
        try {
            if (uploadedFile != null && !uploadedFile.getFileName().isEmpty()) {
                String uploadedExtension = FileUtility.getFileExtension(uploadedFile.getFileName());

                uploadDirPath = Paths.get(StorageUtility.getFileSystemPropertyValueDocumentsDirectory());
                logger.debug("Using property value documents directory: " + uploadDirPath.toString());
                if (Files.notExists(uploadDirPath)) {
                    Files.createDirectory(uploadDirPath);
                }
                File uploadDir = uploadDirPath.toFile();

                String originalExtension = "." + uploadedExtension;
                File originalFile = File.createTempFile("document.", originalExtension, uploadDir);
                InputStream input = uploadedFile.getInputstream();
                Files.copy(input, originalFile.toPath(), StandardCopyOption.REPLACE_EXISTING);
                logger.debug("Saved file: " + originalFile.toPath());
                
                GalleryUtility.storeImagePreviews(originalFile, uploadedExtension);
                
                propertyValue.setValue(originalFile.getName());
                SessionUtility.addInfoMessage("Success", "Uploaded file " + uploadedFile.getFileName() + ".");
            }
        } catch (IOException ex) {
            logger.error(ex);
            SessionUtility.addErrorMessage("Error", ex.toString());
        }
    }
    
    public void handleSingleFileUpload(FileUploadEvent event) {
        this.uploadedFile = event.getFile();
    }
}
