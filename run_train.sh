python train.py --event_vector_size 36 \
--rnn_hidden_size 128 \
--classifier_hidden_size 32 \
--encoder_type rnn_selfattention \
--decoder_type concat_linear \
--n_players 15 \
--n_roles 6 \
--train_file_list data/gat2017log15_data/train_file_list \
--validation_file_list data/gat2017log15_data/test_file_list \
--update_frequency 100 \
--loss_scale last_step_only \
--loss_weights uniform \
--gpu_device_number 0 \
--log_frequency 1
