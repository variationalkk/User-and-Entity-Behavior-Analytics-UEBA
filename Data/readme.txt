I choose three users' data for test. And we considered three types of features which includes action features, action sequence and role features.
---------------------------------------
Role_feature.csv: the average of actions features of  all users under the role of "ProductionLineWorker".
Mix_Three_Feature_Loss: combined three users' losses and generated train and test data.
---------------------------------------
Every user's files:

            * ./ device.csv,email.csv,file.csv,http.csv,logon.csv,psychometric.csv are all extracted from CERT/R4.2 directly.

            * new: newly arranged data which came from above.

            * feture/sequence:  
                        data_out.csv,data_all.csv, label.csv are total feature data (generated from files in 'new' folder).
                        data_train.csv,test.csv,label_train.csv,label_test.csv are generated from data_all.csv and label_all.csv 
                        for deep model.
                        predict.csv,predict_all.csv are predictions from trained feature model.
                        loss_all.csv,my_loss.csv are two types of loss caculated by trained model.

            * Model:
                        Action: deep model and tensorboard file for action sequence.
                        Feature: deep model and tensorboard file for action features. 
                        Role_loss: loss caculated by role features.

            * Mix:
                        We spliced these three losses together.
