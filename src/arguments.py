import argparse

#Checkout https://github.com/awslabs/sockeye/blob/master/sockeye/arguments.py and https://stackoverflow.com/questions/28579661/getting-required-option-from-namespace-in-python

def add_arguments(parser):
    # Model parameters
    parser.add_argument("--event_vector_size",type=int,help="Size of each of the event vectors")
    parser.add_argument("--rnn_hidden_size",type=int,help="Hidden size of the RNN layers")
    parser.add_argument("--encoder_type", type=str, choices=["rnn","rnn_selfattention"], help="Type of encoder architecture")
    parser.add_argument("--decoder_type", type=str, choices=["linear", "concat_linear"],
                        help="Type of decoder architecture")
    parser.add_argument("--classifier_hidden_size",type=int,help="Size of the classifier layers")
    
    
    # Problem parameters
    parser.add_argument("--n_players",type=int,help="Number of players in the game")
    parser.add_argument("--n_roles",type=int,help="Number of possible roles (classes)")
    parser.add_argument("--reduce_classes", dest='reduce_classes', default=False, action='store_true')


    # Training
    parser.add_argument("--update_frequency",type=int,help="Gradient accomulation.Simulates batch size")
    parser.add_argument("--loss_scale",type=str,choices=["last_step_only","uniform","linearly_growing"],help="Type of loss used for training the model.")
    parser.add_argument("--loss_weights",type=str,choices=["uniform","inverse_frequency"])
    parser.add_argument("--log_frequency",type=int,default=100,required=False,help="Show training statistics every log_frequency updates")
    parser.add_argument("--gpu_device_number",type=int,required=False,default=-1,help="Ordinal device number of gpu. Negative number means use CPU")
    parser.add_argument("--train_file_list", type=str,help="File containing the paths of the training files (File list format: One file per line)")

    # Validation
    parser.add_argument("--validation_file_list", type=str,help="File containing the paths of the validation files (File list format: One file per line)")

