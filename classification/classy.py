def TwoByTwo_cm_printouts(cm):
    """For 2x2 cm's ONLY. Prints out stats."""
    print('These stats are for 1 being what is considered positive.')
    true_positive = cm[1][1]
    true_negative = cm[0][0]
    false_positive = cm[0][1]
    false_negative = cm[1][0]
    print(f'accuracy: {(true_positive + true_negative)/(true_positive + true_negative + false_positive + false_negative)}')
    print(f'true positive rate: {true_positive/(true_positive + false_negative)}')
    print(f'false positive rate: {false_positive/(false_positive + true_negative)}')
    print(f'true negative rate: {true_negative/(true_negative + false_positive)}')
    print(f'false negative rate: {false_negative/(false_negative + true_positive)}')
    print(f'precision: {true_positive/(true_positive + false_positive)}')
    print(f'recall: {true_positive/(true_positive + false_negative)}')
    print(f'f1-score: {((true_positive/(true_positive + false_positive)) + (true_positive/(true_positive + false_negative)))/2}')
    print(f'support:\n    did not survive: {true_negative + false_positive}\n    survivied: {true_positive + false_negative}')