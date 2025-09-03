<template>
  <div class="progress-container">
    <div class="progress-info">
      <span class="progress-text">{{ label }}</span>
      <span class="progress-percentage">{{ formatPercentage(percentage) }}%</span>
    </div>
    <div class="progress-bar-bg">
      <div 
        class="progress-bar-fill"
        :class="getProgressClass(percentage)"
        :style="{ width: `${Math.min(Math.max(percentage, 0), 100)}%` }"
      >
        <div class="progress-bar-shine"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProgressBar',
  props: {
    percentage: {
      type: Number,
      required: true,
      validator: (value) => value >= 0
    },
    label: {
      type: String,
      default: 'Progresso'
    },
    showPercentage: {
      type: Boolean,
      default: true
    }
  },
  methods: {
    formatPercentage(value) {
      return Math.round(Math.min(Math.max(value, 0), 100))
    },
    getProgressClass(percentage) {
      if (percentage >= 100) return 'progress-complete'
      if (percentage >= 70) return 'progress-high'
      if (percentage >= 40) return 'progress-medium'
      if (percentage > 0) return 'progress-low'
      return 'progress-none'
    }
  }
}
</script>

<style scoped>
.progress-container {
  width: 100%;
  margin: 8px 0;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  font-size: 0.875rem;
}

.progress-text {
  color: #374151;
  font-weight: 500;
}

.progress-percentage {
  color: #6B7280;
  font-weight: 600;
}

.progress-bar-bg {
  width: 100%;
  height: 8px;
  background: linear-gradient(to right, #f3f4f6, #e5e7eb);
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-bar-fill {
  height: 100%;
  border-radius: 20px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.progress-bar-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shine 2s infinite;
}

/* Cores baseadas no progresso */
.progress-none {
  background: #e5e7eb;
}

.progress-low {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.progress-medium {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.progress-high {
  background: linear-gradient(135deg, #10b981, #059669);
}

.progress-complete {
  background: linear-gradient(135deg, #22c55e, #16a34a);
}

@keyframes shine {
  0% {
    left: -100%;
  }
  50% {
    left: 100%;
  }
  100% {
    left: 100%;
  }
}

/* Responsividade */
@media (max-width: 640px) {
  .progress-info {
    font-size: 0.8rem;
  }
  
  .progress-bar-bg {
    height: 6px;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .progress-text {
    color: #f9fafb;
  }
  
  .progress-percentage {
    color: #d1d5db;
  }
  
  .progress-bar-bg {
    background: linear-gradient(to right, #374151, #4b5563);
  }
}

/* Explicit dark mode classes */
.dark-mode .progress-text {
  color: #f9fafb;
}

.dark-mode .progress-percentage {
  color: #d1d5db;
}

.dark-mode .progress-bar-bg {
  background: linear-gradient(to right, #374151, #4b5563);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

.dark-mode .progress-none {
  background: #4b5563;
}

.dark-mode .progress-bar-shine {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
}
</style>