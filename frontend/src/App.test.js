import { describe, it, expect, vi } from 'vitest'
import { render, fireEvent } from '@testing-library/vue'
import App from './App.vue'

describe('App', () => {
  beforeEach(() => {
    // Mock fetch before each test
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    )
  })

  it('changes service and displays correct title', async () => {
    const { getByText, getAllByRole } = render(App)
    
    // Initially shows Netflix
    expect(getByText('Netflix Shows Leaving Soon')).toBeDefined()
    
    // Change to HBO - get all selects and use the second one (service selector)
    const selects = getAllByRole('combobox')
    await fireEvent.update(selects[1], 'hbo')
    
    expect(getByText('HBO Shows Leaving Soon')).toBeDefined()
  })

  it('shows no data message when titles are empty', async () => {
    const { getByText } = render(App)
    
    expect(getByText('No leaving shows at the moment')).toBeDefined()
  })
}) 