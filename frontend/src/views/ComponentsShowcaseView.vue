<template>
  <div class="showcase">
    <h1>UI Components Showcase</h1>
    <p class="showcase__intro">
      All components use CSS variables from theme.css. Switch themes to see them adapt.
    </p>

    <!-- Buttons -->
    <section class="showcase__section">
      <h2>Buttons</h2>
      <div class="showcase__grid">
        <UiButton variant="primary">Primary Button</UiButton>
        <UiButton variant="secondary">Secondary Button</UiButton>
        <UiButton variant="ghost">Ghost Button</UiButton>
        <UiButton variant="destructive">Destructive Button</UiButton>
        <UiButton variant="primary" disabled>Disabled Button</UiButton>
        <UiButton variant="primary" full-width>Full Width Button</UiButton>
      </div>
    </section>

    <!-- Inputs -->
    <section class="showcase__section">
      <h2>Inputs</h2>
      <div class="showcase__grid">
        <UiInput
          v-model="inputValue"
          label="Email"
          placeholder="Enter your email"
          hint="We'll never share your email"
        />
        <UiInput
          v-model="inputError"
          label="Username"
          placeholder="Enter username"
          error="Username is already taken"
        />
        <UiInput
          v-model="inputDisabled"
          label="Disabled Input"
          disabled
        />
        <UiInput
          v-model="inputFullWidth"
          label="Full Width Input"
          placeholder="This spans the full width"
          full-width
        />
      </div>
    </section>

    <!-- Select -->
    <section class="showcase__section">
      <h2>Select</h2>
      <div class="showcase__grid">
        <UiSelect
          v-model="selectValue"
          label="Choose a fruit"
          placeholder="Select one..."
          :options="selectOptions"
          hint="Pick your favorite"
        />
        <UiSelect
          v-model="selectError"
          label="Choose a color"
          :options="colorOptions"
          error="This field is required"
        />
        <UiSelect
          v-model="selectDisabled"
          label="Disabled Select"
          :options="selectOptions"
          disabled
        />
      </div>
    </section>

    <!-- Semantic Colors -->
    <section class="showcase__section">
      <h2>Semantic Color Palettes</h2>
      <p class="showcase__description">
        Our semantic color system uses consistent 3-shade palettes for all alert states.
      </p>
      <div class="showcase__color-grid">
        <div class="showcase__color-card">
          <div class="showcase__color-swatch" style="background: var(--success-border)"></div>
          <div class="showcase__color-swatch" style="background: var(--success-bg)"></div>
          <div class="showcase__color-swatch" style="background: var(--success-muted)"></div>
          <div class="showcase__color-label">Success</div>
        </div>
        <div class="showcase__color-card">
          <div class="showcase__color-swatch" style="background: var(--warning-border)"></div>
          <div class="showcase__color-swatch" style="background: var(--warning-bg)"></div>
          <div class="showcase__color-swatch" style="background: var(--warning-muted)"></div>
          <div class="showcase__color-label">Warning</div>
        </div>
        <div class="showcase__color-card">
          <div class="showcase__color-swatch" style="background: var(--danger-border)"></div>
          <div class="showcase__color-swatch" style="background: var(--danger-bg)"></div>
          <div class="showcase__color-swatch" style="background: var(--danger-muted)"></div>
          <div class="showcase__color-label">Danger</div>
        </div>
        <div class="showcase__color-card">
          <div class="showcase__color-swatch" style="background: var(--info-border)"></div>
          <div class="showcase__color-swatch" style="background: var(--info-bg)"></div>
          <div class="showcase__color-swatch" style="background: var(--info-muted)"></div>
          <div class="showcase__color-label">Info</div>
        </div>
      </div>
    </section>

    <!-- Alerts -->
    <section class="showcase__section">
      <h2>Alerts with Semantic Colors</h2>
      <div class="showcase__stack">
        <UiAlert variant="info" dismissible @dismiss="() => {}">
          <strong>Info:</strong> This is an informational alert using our semantic info palette.
        </UiAlert>
        <UiAlert variant="success" dismissible @dismiss="() => {}">
          <strong>Success!</strong> Your changes have been saved successfully.
        </UiAlert>
        <UiAlert variant="warning" dismissible @dismiss="() => {}">
          <strong>Warning:</strong> This action cannot be undone. Please proceed with caution.
        </UiAlert>
        <UiAlert variant="error" dismissible @dismiss="() => {}">
          <strong>Error:</strong> Something went wrong. Please try again or contact support.
        </UiAlert>
      </div>
    </section>

    <!-- Toast Demo -->
    <section class="showcase__section">
      <h2>Toast Notifications</h2>
      <p class="showcase__description">
        Click the buttons below to see toast notifications with semantic colors.
      </p>
      <div class="showcase__grid">
        <UiButton variant="secondary" @click="showInfoToast">Show Info Toast</UiButton>
        <UiButton variant="secondary" @click="showSuccessToast">Show Success Toast</UiButton>
        <UiButton variant="secondary" @click="showWarningToast">Show Warning Toast</UiButton>
        <UiButton variant="secondary" @click="showErrorToast">Show Error Toast</UiButton>
      </div>
    </section>

    <!-- Cards -->
    <section class="showcase__section">
      <h2>Cards</h2>
      <div class="showcase__grid">
        <UiCard>
          <template #header>Card with Header</template>
          <p>This is the card body content. It can contain any content you want.</p>
          <template #footer>
            <UiButton variant="secondary">Cancel</UiButton>
            <UiButton variant="primary">Save</UiButton>
          </template>
        </UiCard>

        <UiCard>
          <p>This is a simple card with just body content, no header or footer.</p>
        </UiCard>
      </div>
    </section>

    <!-- Spinner -->
    <section class="showcase__section">
      <h2>Spinner</h2>
      <div class="showcase__grid">
        <div class="showcase__spinner-demo">
          <UiSpinner size="sm" />
          <span>Small</span>
        </div>
        <div class="showcase__spinner-demo">
          <UiSpinner size="md" />
          <span>Medium</span>
        </div>
        <div class="showcase__spinner-demo">
          <UiSpinner size="lg" />
          <span>Large</span>
        </div>
      </div>
    </section>

    <!-- Modal -->
    <section class="showcase__section">
      <h2>Modal</h2>
      <UiButton variant="primary" @click="showModal = true">Open Modal</UiButton>
      <UiModal
        v-model="showModal"
        title="Example Modal"
        :primary-action="{ label: 'Confirm', onClick: handleModalConfirm }"
        :secondary-action="{ label: 'Cancel', onClick: () => showModal = false }"
      >
        <p>This is a modal dialog with a title, content, and action buttons.</p>
        <p>It includes basic ARIA attributes for accessibility.</p>
      </UiModal>
    </section>

    <!-- State Components -->
    <section class="showcase__section">
      <h2>State Components</h2>
      <div class="showcase__stack">
        <UiCard>
          <template #header>Loading State</template>
          <UiLoadingState message="Loading your data..." />
        </UiCard>

        <UiCard>
          <template #header>Error State</template>
          <UiErrorState
            title="Failed to load data"
            message="There was a problem connecting to the server."
            retry-label="Try Again"
            @retry="handleRetry"
          />
        </UiCard>

        <UiCard>
          <template #header>Empty State</template>
          <UiEmptyState
            title="No items yet"
            message="Start by creating your first item."
            action-label="Create Item"
            icon="📦"
            @action="handleAction"
          />
        </UiCard>
      </div>
    </section>

    <!-- Form Section -->
    <section class="showcase__section">
      <h2>Form Section</h2>
      <UiCard>
        <template #header>User Profile Form</template>
        <UiFormSection>
          <UiInput
            v-model="formName"
            label="Full Name"
            placeholder="Enter your name"
            full-width
          />
          <UiInput
            v-model="formEmail"
            label="Email Address"
            type="email"
            placeholder="you@example.com"
            hint="We'll never share your email"
            full-width
          />
          <UiSelect
            v-model="formRole"
            label="Role"
            placeholder="Select a role..."
            :options="roleOptions"
            full-width
          />
          <template #actions>
            <UiButton variant="secondary">Cancel</UiButton>
            <UiButton variant="primary">Save Changes</UiButton>
          </template>
        </UiFormSection>
      </UiCard>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import UiButton from '../components/UiButton.vue';
import UiInput from '../components/UiInput.vue';
import UiSelect from '../components/UiSelect.vue';
import UiAlert from '../components/UiAlert.vue';
import UiCard from '../components/UiCard.vue';
import UiSpinner from '../components/UiSpinner.vue';
import UiModal from '../components/UiModal.vue';
import UiLoadingState from '../components/UiLoadingState.vue';
import UiErrorState from '../components/UiErrorState.vue';
import UiEmptyState from '../components/UiEmptyState.vue';
import UiFormSection from '../components/UiFormSection.vue';
import { useToasts } from '../composables/useToasts';

const inputValue = ref('');
const inputError = ref('john_doe');
const inputDisabled = ref('Disabled value');
const inputFullWidth = ref('');

const selectValue = ref('');
const selectError = ref('');
const selectDisabled = ref('apple');

const selectOptions = [
  { value: 'apple', label: 'Apple' },
  { value: 'banana', label: 'Banana' },
  { value: 'orange', label: 'Orange' },
  { value: 'grape', label: 'Grape' },
];

const colorOptions = [
  { value: 'red', label: 'Red' },
  { value: 'blue', label: 'Blue' },
  { value: 'green', label: 'Green' },
];

const showModal = ref(false);

const formName = ref('');
const formEmail = ref('');
const formRole = ref('');

const roleOptions = [
  { value: 'admin', label: 'Administrator' },
  { value: 'user', label: 'User' },
  { value: 'guest', label: 'Guest' },
];

const { info, success, warning, error } = useToasts();

const handleModalConfirm = () => {
  alert('Modal confirmed!');
  showModal.value = false;
};

const handleRetry = () => {
  alert('Retry clicked');
};

const handleAction = () => {
  alert('Action clicked');
};

const showInfoToast = () => {
  info('This is an informational message with semantic colors.');
};

const showSuccessToast = () => {
  success('Operation completed successfully!');
};

const showWarningToast = () => {
  warning('Please review this warning before proceeding.');
};

const showErrorToast = () => {
  error('An error occurred. Please try again.');
};
</script>

<style scoped>
.showcase {
  max-width: 1200px;
  margin: 0 auto;
}

.showcase h1 {
  color: var(--color-text);
  margin-bottom: var(--space-sm);
  font-size: 1.75rem;
}

.showcase__intro {
  color: var(--color-text-muted);
  margin-bottom: var(--space-xl);
  font-size: 0.875rem;
}

.showcase__section {
  margin-bottom: var(--space-xl);
}

.showcase__section h2 {
  color: var(--color-text);
  margin-bottom: var(--space-lg);
  font-size: 1.25rem;
}

.showcase__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-md);
}

.showcase__stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.showcase__spinner-demo {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--border-radius-md);
}

.showcase__spinner-demo span {
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.showcase__description {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-bottom: var(--space-md);
}

.showcase__color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--space-md);
}

.showcase__color-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-md);
  background: var(--color-surface);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-surface-soft);
}

.showcase__color-swatch {
  height: 2.5rem;
  border-radius: var(--border-radius-sm);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.showcase__color-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text);
  text-align: center;
  margin-top: var(--space-xs);
}

@media (min-width: 640px) {
  .showcase__grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--space-lg);
  }

  .showcase h1 {
    font-size: 2rem;
  }

  .showcase__section h2 {
    font-size: 1.5rem;
  }

  .showcase__intro,
  .showcase__description {
    font-size: 1rem;
  }

  .showcase__color-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
