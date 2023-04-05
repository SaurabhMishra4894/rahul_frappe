frappe.pages['tenant-management'].on_page_load = (wrapper) => {
	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Tenant Management'),
		card_layout: true,
		single_column: true
	});

	wrapper.tenant_engine = new frappe.TenantEngine(wrapper);

};


frappe.TenantEngine = class TenantEngine {
	constructor(wrapper) {
		this.wrapper = wrapper;
		this.page = wrapper.page;
		this.body = $(this.wrapper).find(".tenant_management");
		this.fetch_messages_then_render();

	}

	make() {
		frappe.call({
			method: "frappe.tenant_management.doctype.tenant.tenant.tenant_data"
		}).then((res) => {
			console.log("2222 "+res.message.total_income);
			this.tenants = res.message;
		});
	}



	fetch_messages_then_render() {
		this.fetch_messages().then(messages => {
			this.messages = messages;
			$('<div class="tenant_management"></div>').appendTo(this.page.main);
			$(frappe.render_template("tenant_management", {"messages":messages})).appendTo(this.page.main);
		});
	}

	fetch_messages() {
		frappe.dom.freeze(__('Fetching...'));
		return frappe
			.xcall('frappe.tenant_management.doctype.tenant.tenant.tenant_data')
			.then(messages => {
				return messages;
			})
			.finally(() => {
				frappe.dom.unfreeze();
			});
	}

	render_messages(messages) {
		let template = message => `
			<div class="total_income_card">
                        <p>Total Income (This Month)</p>
                        <p>₹ ${message}</p>
                    </div>
		`;
		this.body.find('.total_income_card').html([messages.total_data.total_income].map(template).join(''));
		let template2 = message => `
			<div class="total_expense_card">
                        <p>Total Expenses (This Month)</p>
                        <p style="color: red">₹ ${message}</p>
                    </div>
		`;
		this.body.find('.total_expense_card').html([messages.total_data.total_expenses].map(template2).join(''));
		let template3 = message => `
			<div class="total_dues_card">
                        <p>Total Dues (This Month)</p>
                        <p>₹ ${message}</p>
                    </div>
		`;
		this.body.find('.total_dues_card').html([messages.total_data.total_dues].map(template3).join(''));

	}
}

