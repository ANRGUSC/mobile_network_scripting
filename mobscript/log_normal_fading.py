import math
from typing import Dict, List, Union
from .data_structures.unit import Unit
from math import erfc, sqrt
from math import sqrt, erfc
from scipy.special import erfcinv
import heapq
import pygame

class ShannonCapacity:
    def capacity_calculation(self, P_t, K, n, d, d_0, sigma, bandwidth):
            pathloss_dB = 10*n*math.log10(d/d_0) + 10*K*math.log10(d_0) 
            pathloss_ratio = 10**(-pathloss_dB/10)
            self.shannon_capacity = round(bandwidth*math.log2(1 + P_t*pathloss_ratio/sigma), 4)
            return self.shannon_capacity

class CalculateMetrics:
    def bit_error_probability(self, P_t, snr,d ,d_0, K, sigma, bandwidth,n):
        self.bit_error_prob = round(0.5 * erfc(sqrt(2 * snr)), 4)
        return self.bit_error_prob

    def packet_error_probability(self, snr, num_bits, packet_size, P_t, d ,d_0, K, sigma, bandwidth,n):
        ber = self.bit_error_probability(P_t, snr,d ,d_0, K, sigma, bandwidth,n)     
        self.pep = round(1 - (1 - ber)**(num_bits/packet_size), 4)
        return self.pep

    def calculate_ETX(self):
        self.etx = round(1 / (1 - self.pep), 4)
        return self.etx