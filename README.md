# MCI_Analysis
The MCI analysis toolkit contains a python program to process formatted .csv files with acceleration data to detect MCI suggestive abnormal movement patterns.

## Introduction

>MCI is an intermediate stage of brain malfunction between normal aging and more serious
dementia, of which the most common one is Alzheimer’s disease. Current diagnosis relies
heavily on clinical observations which is usually time-consuming. Effective computer aided MCI
classification therefore is much desired in facilitate the diagnosis process.
Body motion detection using accelerometers has drawn considerable attention as an alternative
of visual information based movement recognition. With accelerometers, we can collect motion
data including azimuth, pitch, roll, and acceleration along x, y and z rotation vectors of the
device. Different patterns of movements yield different results, it’s thus logically possible to
reversely calculate the corresponding motion based on the given acceleration data.
The clinical observations are based on recorded videos of patients preparing breakfast, lunch, etc.
in prearranged environment settings. Experts then examine the videos closely to find abnormal
MCI suggestive behaviors. This process can be greatly facilitated if we can collect data that
contains information about the patient’s movement patterns and have them analyzed
automatically with a computer program. The most distinguishable features from the clinical
observations are pauses and sudden moves. During the laboratory assessments, the patients wear
a smartwatch that collects acceleration data. We then feed the data into our classification
algorithms to analyze if there are suspicious movement patterns such as more pauses and
direction changes. The results of our analysis suggest that MCI patients pause and change
directions more often based on the patterns of their hand movements. Certain subtasks are
complicated and require more attention than other tasks, and MCI patients are prone to make
more mistakes that resulting in more direction changes and pauses that can be reflected from the
acceleration data. Some of these subtasks are identified in our study and we believe the research
is beneficial in cutting down the time and resources put into clinical MCI diagnosis.
The diagnosis of MCI is by far largely clinical based on a doctor’s professional judgement. A
doctor typically needs to examine the patient’s detailed medical history for any previous medical
conditions or family history of memory problems or dementia. This is combined with brief tests
that assess mental status and neurological conditions. Sometimes laboratory tests such as blood
tests and neuroimaging are performed as ancillary testing to further assess a patient’s cognitive
conditions. Since neuropsychological tests are an important part of MCI diagnosis, it’s desirable
that the tests results can be automatically analyzed by a computer. As an initial exploration, our
goal in this study is to find the difference of movement patterns between MCI patients and
normal people, thus providing more clues that leads to successful MCI diagnosis.

## Data collection and preprocessing
>Studies have shown that the occurrence of MCI is very rare, with a ratio of less than 7.2% per
100 non-demented persons.Understandably MCI patients are very difficult to find, we
therefore used data collected from participants who imitate MCI patients. Our participants
constitute 18 young adults for each group: MCI patients and normal people. They imitate MCI
patients by entering a mentally equivalent status after purposely getting distracted.[8]
All the data are from clinical tests. They are collected using a smartwatch our subjects wear on
their wrists. The tests are designed specially to test the subjects’ cognitive capabilities. Table 1
below shows a sample subset of the data:
