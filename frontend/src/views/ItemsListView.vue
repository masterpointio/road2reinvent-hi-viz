<template>
  <div class="items-list">
    <div class="items-list__header">
      <h1>Items</h1>
      <UiButton variant="primary" @click="handleRefresh">
        Refresh
      </UiButton>
    </div>

    <UiCard>
      <UiLoadingState v-if="isLoading" message="Loading items..." />

      <UiErrorState
        v-else-if="error"
        :message="error"
        retry-label="Try Again"
        @retry="refetch"
      />

      <UiEmptyState
        v-else-if="!data || data.length === 0"
        title="No items found"
        message="Get started by adding your first item."
        action-label="Add First Item"
        @action="handleAddItem"
      />

      <div v-else class="items-list__table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in data" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.description || '-' }}</td>
              <td>
                <span :class="['status-badge', `status-badge--${item.status}`]">
                  {{ item.status }}
                </span>
              </td>
              <td>
                <div class="items-list__actions">
                  <UiButton variant="ghost" @click="handleEdit(item)">
                    Edit
                  </UiButton>
                  <UiButton variant="ghost" @click="handleDelete(item)">
                    Delete
                  </UiButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UiCard>
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue';
import { useApi } from '../composables/useApi';
import { useQuery } from '../composables/useQuery';
import { useToasts } from '../composables/useToasts';
import UiCard from '../components/UiCard.vue';
import UiButton from '../components/UiButton.vue';
import UiLoadingState from '../components/UiLoadingState.vue';
import UiErrorState from '../components/UiErrorState.vue';
import UiEmptyState from '../components/UiEmptyState.vue';

interface Item {
  id: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive' | 'pending';
}

const api = useApi();
const { success, error: showError } = useToasts();

const { data, isLoading, error, refetch } = useQuery<Item[]>(
  () => api.get('/items')
);

watch(error, (newError) => {
  if (newError) {
    showError(`Failed to load items: ${newError}`);
  }
});

const handleRefresh = async () => {
  await refetch();
  if (!error.value) {
    success('Items refreshed successfully');
  }
};

const handleAddItem = () => {
  success('Add item feature coming soon!');
};

const handleEdit = async (item: Item) => {
  try {
    await api.put(`/items/${item.id}`, { ...item, name: `${item.name} (edited)` });
    success(`Item "${item.name}" updated successfully`);
    refetch();
  } catch (err: any) {
    showError(`Failed to update item: ${err.message}`);
  }
};

const handleDelete = async (item: Item) => {
  if (!confirm(`Are you sure you want to delete "${item.name}"?`)) {
    return;
  }

  try {
    await api.del(`/items/${item.id}`);
    success(`Item "${item.name}" deleted successfully`);
    refetch();
  } catch (err: any) {
    showError(`Failed to delete item: ${err.message}`);
  }
};
</script>

<style scoped>
.items-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.items-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.items-list__header h1 {
  margin: 0;
  color: var(--color-text);
}

.items-list__table {
  overflow-x: auto;
}

.items-list__table table {
  width: 100%;
  border-collapse: collapse;
}

.items-list__table th {
  text-align: left;
  padding: var(--space-md);
  border-bottom: 2px solid var(--color-surface-soft);
  color: var(--color-text);
  font-weight: 600;
  font-size: 0.875rem;
}

.items-list__table td {
  padding: var(--space-md);
  border-bottom: 1px solid var(--color-surface-soft);
  color: var(--color-text);
  font-size: 0.875rem;
}

.items-list__table tbody tr:hover {
  background: var(--color-surface-soft);
}

.items-list__actions {
  display: flex;
  gap: var(--space-xs);
}

.status-badge {
  display: inline-block;
  padding: var(--space-xs) var(--space-sm);
  border-radius: var(--border-radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge--active {
  background: var(--success-bg);
  color: var(--text-on-success);
  border: 1px solid var(--success-border);
}

.status-badge--inactive {
  background: var(--danger-bg);
  color: var(--text-on-danger);
  border: 1px solid var(--danger-border);
}

.status-badge--pending {
  background: var(--warning-bg);
  color: var(--text-on-warning);
  border: 1px solid var(--warning-border);
}
</style>
